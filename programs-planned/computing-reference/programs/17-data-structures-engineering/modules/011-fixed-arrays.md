---
module_id: DSE-011
program: Data Structures Engineering
level: 1
module_number: 11
title: Fixed Arrays
status: complete
last_verified: 2026-08-29
---

# Fixed Arrays

## One-Page Review

### Governing question

How should a fixed array's extent, layout, indexing, initialization, ownership, bounds, and lifetime be specified so that constant-time position access remains correct across languages, representations, and interfaces?

### Essential definitions

- A **fixed array** is a finite indexed sequence of homogeneous element slots whose extent does not change during that array value's lifetime.
- The **extent** $n$ is the number of slots; valid zero-based indices satisfy $0\le i<n$.
- A **contiguous array representation** places equal-size element slots consecutively, so slot $i$ has byte offset $i s$ for slot size $s$, subject to valid arithmetic and layout rules.
- A **slice/view** describes some array storage using a base, length, and possibly strides; it need not own the storage or preserve the array's full extent in its type.
- A **stride** is the byte displacement for increasing one dimension's index by one. Contiguity is one stride configuration, not a synonym for every multidimensional view.
- **bounds checking** verifies an index before memory access. Failure may be a language exception, panic, optional result, trap, or rejected operation; unchecked access has a different contract.
- **array decay** is a language conversion that replaces an array expression with a pointer to an element in many contexts, losing extent unless carried separately.
- **partial initialization** is a low-level state in which only a prefix or subset of slots contains live elements; construction and destruction must track it exactly.
- **array covariance** permits an array of a subtype to be treated as an array of a supertype; mutation then requires a dynamic store check or risks unsoundness.
- **one-past-the-end** is a position useful for iteration in some low-level language contracts. It is not a valid element to dereference.

### Central model, mechanism, or theorem

The abstract value is $A=\langle a_0,\ldots,a_{n-1}\rangle$. Under a contiguous uniform-slot representation with base address $B$ and slot size $s$, valid element access computes

$$
addr(A[i])=B+i s,\qquad 0\le i<n.
$$

This gives constant abstract address computation, not constant end-to-end latency across cache, page, device, or remote-memory regimes. Correctness requires that $n$, $s$, multiplication, addition, allocation size, alignment, provenance, initialization, lifetime, and bounds all satisfy their representation contracts.

For a row-major $R\times C$ matrix, $offset(r,c)=(rC+c)s$. More generally, a $d$-dimensional strided view has

$$
offset(i_0,\ldots,i_{d-1})=o+\sum_{k=0}^{d-1} i_k t_k,
$$

where $o$ is a base offset and $t_k$ are byte strides.

### Critical invariants

1. Extent is fixed and every accepted index is in the declared domain.
2. Allocation size and every address calculation are checked for overflow before access.
3. Each live slot contains exactly one valid element; uninitialized storage is never read as a value.
4. Each constructed element is destroyed exactly once, including exceptional or partial construction.
5. Views cannot outlive their storage, and mutable aliases obey the language's exclusivity or synchronization rules.
6. Layout, alignment, byte order, and ABI claims are made only where the governing specification guarantees them.
7. Multidimensional shape and strides map valid logical indices to valid storage without unintended overlap, unless overlap is explicitly supported.

### Common failures

- Equating fixed extent with immutable elements.
- Assuming every fixed array is stack allocated or every dynamic-length array is heap allocated.
- Losing extent through a raw pointer and trusting a caller-provided length.
- Checking `i < n` with a signed negative index that converts to a large unsigned value.
- Allowing `n * sizeof(T)` or a multidimensional product to overflow before allocation.
- Reading uninitialized slots or dropping elements that were never constructed.
- Dereferencing one-past-the-end or forming pointers outside the permitted object domain.
- Assuming a nested reference array is rectangular, flat, or contiguous.
- Treating a transposed/strided view as contiguous at an FFI boundary.
- Sharing adjacent writable elements across threads without considering data races or false sharing.

### Compact example

A fixed `int32` matrix with shape $2\times3$ in row-major layout has element size 4 bytes, row stride 12 bytes, column stride 4 bytes, and 24 bytes of element storage. Logical index `(1,2)` maps to flat index `1*3+2=5` and byte offset `5*4=20`. The access is valid because `0<=1<2` and `0<=2<3`; `(2,0)` is rejected before calculating or using an address.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) supplies the sequence abstraction, [DSE-002](002-representation-invariants.md) supplies valid-state obligations, [DSE-003](003-operation-contracts.md) supplies checked and unchecked failure semantics, [DSE-004](004-time-space-and-allocation-cost.md) supplies cost dimensions, [DSE-005](005-contiguous-and-linked-layouts.md) supplies layout alternatives, and [DSE-006](006-memory-locality-and-cache-behavior.md) supplies measured access behavior. DSE-012 adds resizing; later sequence modules change mutation and position trade-offs.

## Governing Question

What exactly is fixed in a fixed array, which representation and language guarantees make indexed access valid, and what must an engineer prove or check at ownership, initialization, view, FFI, and concurrency boundaries?

## Why This Matters

Arrays sit beneath strings, tensors, image buffers, packet fields, database pages, virtual-machine stacks, lookup tables, and nearly every higher-level sequence. Their address formula looks elementary, which makes array defects deceptively easy to underestimate. The formula is useful only when the index, extent, element layout, arithmetic, allocation, initialization, and lifetime agree. A single mismatch can become silent corruption in an unchecked language, a controlled exception in another, or an optimization invalidation when undefined behavior enters the program.

Fixed extent also enables strong engineering: size can participate in types, storage can be embedded inline, iteration bounds can be proved, layouts can cross carefully governed ABIs, and compilers can unroll or vectorize. Yet none of these consequences is universal. Java array length is a runtime property rather than part of the type; Rust `[T; N]` and Go `[N]T` include extent in the type; C expressions often decay to pointers; nested Java arrays are arrays of references and can be ragged. Graduate-level reasoning starts by naming the exact model in force.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstract sequences, abstraction functions, and observational equivalence from [DSE-001](001-abstract-data-types-and-concrete-representations.md);
- representation invariants and valid-state transitions from [DSE-002](002-representation-invariants.md);
- indexing, failure, mutation, aliasing, and resource contracts from [DSE-003](003-operation-contracts.md);
- time, space, allocation, overflow, and tail-cost reasoning from [DSE-004](004-time-space-and-allocation-cost.md);
- contiguous layout, alignment, ownership, views, and linked alternatives from [DSE-005](005-contiguous-and-linked-layouts.md);
- locality hypotheses and evidence limits from [DSE-006](006-memory-locality-and-cache-behavior.md);
- type constraints and traversal protocols from [DSE-007](007-genericity-and-type-constraints.md) and [DSE-008](008-iterators-and-traversal-protocols.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify a fixed array as an abstract sequence plus an explicit concrete representation;
2. derive one- and multidimensional address formulas and state every precondition they require;
3. distinguish fixed extent, storage placement, mutability, ownership, and contiguity;
4. compare checked, unchecked, panicking, trapping, and result-returning index APIs;
5. reason about zero-length arrays, one-past positions, signed/unsigned indices, size overflow, alignment, and provenance;
6. design total initialization and exception-safe partial initialization/destruction;
7. distinguish owning arrays from slices, spans, pointers, and strided views and control their lifetimes;
8. explain important Rust, C, C++, Java, Go, and numerical-array semantic differences without forcing a false common model;
9. design array tests, sanitization, static checks, benchmarks, and FFI records appropriate to the claim;
10. evaluate concurrent, security-sensitive, and high-stakes uses without overclaiming from layout or finite tests.

## Core Exposition

**Begin with the abstract sequence.** For element domain $T$ and extent $n\ge0$, define $A\in T^n$. `get(i)` requires $0\le i<n$ and returns $a_i$. `set(i,x)` under a mutable contract produces the sequence whose position $i$ is $x$ and whose other positions are unchanged. Length remains $n$. Iteration yields positions in a declared order, ordinarily increasing index. This model says nothing yet about bytes, storage region, language exceptions, or cache behavior.

“Fixed” qualifies extent, not value. Elements may be mutable; an immutable array may still contain references to mutable objects; and a fixed array value may itself be replaced, moved, copied, or referenced under language rules. Conversely, a dynamically allocated Java array has fixed length after creation. Storage duration and extent mutability are orthogonal.

**Choose the representation deliberately.** The core low-level representation is $n$ homogeneous slots stored consecutively. If type $T$ has slot size $s$ and required alignment $a$, the array begins at a suitably aligned base and occupies $n s$ element bytes when the language layout says so. Each slot begins at $B+i s$. The slot size already incorporates any padding needed between consecutive elements; do not add a second invented padding term.

Not all values called “arrays” expose that physical guarantee. A managed runtime can specify logical components and bounds without promising an ABI-visible object layout. A nested array can store references to separate row arrays. A numerical array view can expose homogeneous fixed-size items with arbitrary positive, negative, or zero-like broadcast strides subject to its library contract. Write “contiguous inline fixed array” when physical adjacency is part of the claim.

**Validate address arithmetic before using it.** A safe access sequence is conceptual:

1. validate or establish $0\le i<n$;
2. establish that $n s$ was representable and sufficient when storage was allocated;
3. establish that $i s$ and $B+i s$ satisfy the language's integer and pointer rules;
4. establish alignment, provenance, lifetime, initialization, and access permission;
5. load or store exactly one `T` under its representation rules.

Checking only the final pointer is too late if intermediate signed overflow is undefined or unsigned arithmetic wrapped. Prefer checked multiplication/addition and compare without dangerous conversions. For a signed index, `i >= 0 && converted_i < n` is different from converting first and checking only `< n`. APIs accepting byte counts must verify both element-count and byte-count limits.

Some low-level languages permit forming a pointer one position beyond an array for iteration/comparison, but not dereferencing it. Permission to compute other out-of-range addresses varies by language and intermediate representation. LLVM's `getelementptr` computes addresses without loading memory; its `inbounds` promises are about the actual allocated object and overflow, not a runtime bounds check derived solely from the static array type. Front ends must translate source rules correctly.

**Bounds policy is an API decision.** A checked accessor can throw, panic, trap, or return an optional/error. Each affects composition, cleanup, real-time behavior, and denial-of-service exposure. An unchecked accessor can remove repeated checks when a stronger caller proof exists, but it transfers a proof obligation: valid index, live initialized element, aligned in-bounds storage, and permitted aliasing. Put unchecked operations behind narrow interfaces, document invariants, and test them under sanitizers or interpreters capable of detecting memory violations.

Languages differ materially. Safe Rust array indexing is bounds checked and all array elements are initialized; unchecked raw/slice operations are explicitly unsafe. Java checks every array access at runtime. Go specifies valid index ranges and panics for out-of-range runtime indices. C and C++ built-in subscript operations can have undefined behavior outside the array object; C++ `std::array::at` is checked while `operator[]` carries the ordinary precondition. Do not write a language-neutral statement that “arrays throw” or “arrays are unchecked.”

**Initialization is part of representation validity.** Many safe languages initialize every component at array creation, through explicit elements, repeated values, or language-defined zero/default values. Low-level performance code may reserve raw storage and construct elements one at a time. During partial construction, state includes the set or prefix of initialized slots. If construction of element $k$ fails, exactly elements already constructed must be destroyed; uninitialized bytes must not be read, compared, hashed, serialized, or destroyed as `T`.

For nontrivial elements, copying, moving, replacing, and destroying an array apply element operations under language-specific ordering and failure rules. A bitwise copy is valid only for types whose representation contract permits it. Padding bytes, pointer provenance, ownership tokens, reference counts, file descriptors, and cryptographic secrets make raw byte copying or comparison dangerous. Clearing an array of objects is not necessarily equivalent to zeroing its storage.

Zero extent is mathematically ordinary: $T^0$ contains the empty sequence. Language support differs. Rust `[T; 0]`, Go `[0]T`, Java zero-length arrays, and `std::array<T,0>` are supported, but pointer/data behavior and built-in C array constraints require their own rules. Empty-array `front`, `back`, or element access is invalid. Generic code must not assume a non-null distinct data pointer for every empty representation unless guaranteed.

**Array type identity differs across ecosystems.** Rust `[T; N]` and Go `[N]T` make $N$ part of the type. This supports compile-time extent constraints but means different extents are different types. Java uses `T[]`; length belongs to the object, not the array type. C built-in array declarators encode bounds in declarations, but parameters undergo adjustments and many expressions decay to pointers. C++ `std::array<T,N>` retains extent as a template parameter and behaves as an aggregate container.

Copy semantics also differ. Go array assignment copies the array value when element semantics permit. Rust arrays follow move/copy rules of the element type and array type. Java variables hold references to array objects; assignment aliases rather than copies components. C built-in arrays are not assignable as whole array values, though an enclosing structure can be copied according to C rules. API documentation must say whether passing an array copies elements, moves ownership, borrows, aliases, or passes a descriptor.

Java reference arrays expose a classic type-safety trade-off. If `Dog[]` is viewed as `Animal[]`, storing a `Cat` through the broader reference must be dynamically rejected because the runtime array remains a `Dog[]`. This covariance plus mutation creates `ArrayStoreException`. Generic containers often choose invariant type parameters instead. Property tests should include subtype stores and distinguish compile-time acceptance from runtime validity.

**Views preserve storage, not ownership by default.** A slice/span commonly stores a pointer/reference and length; a multidimensional view adds shape and strides. Creating a view can be constant time and avoid copying, but aliases the underlying elements. Mutation through one alias can be observed through another. Reallocation, owner destruction, unmapping, device transfer, or scope exit can invalidate the view. Safe borrow systems enforce some lifetimes/exclusivity statically; managed runtimes may retain owners; raw spans rely on discipline.

C array-to-pointer decay illustrates extent loss. A function receiving only `T*` cannot recover the caller's array length from the pointer. Pass a length, a sentinel under a valid element policy, a span-like descriptor, or an extent-carrying type. Validate that the length describes the same allocated object. `sizeof(pointer)` is not array byte size, and a sentinel cannot represent termination safely if every bit pattern is valid data or corruption removes the sentinel.

**Multidimensional arrays are mappings.** For a dense row-major shape $(n_0,\ldots,n_{d-1})$, strides are derived from trailing extents. For a two-dimensional $R\times C$ array of slot size $s$, row stride is $Cs$ and column stride is $s$. Column-major order reverses which dimension is contiguous. A general view stores explicit strides; transpose can swap strides without moving elements.

Validate every dimension, the product of extents, byte size, base offset, and extremal reachable offset using checked arithmetic. A shape product that wraps to a small allocation followed by large logical indexing is a serious vulnerability. Negative strides require a base positioned so valid logical indices stay in the allocation. Overlapping strides can cause multiple logical indices to alias one slot; reject them for independent mutable-element APIs or specify reductions/synchronization.

Nested arrays are not automatically dense matrices. Java `int[][]` is an array whose components reference `int[]` objects; rows can be null or have different lengths. Go and Rust can express nested inline array types with outer extent $R$ and inner extent $C$, under their different language layout guarantees. At FFI boundaries, exchange explicit element type, shape, strides, byte order, alignment, ownership, lifetime, mutability, and address space instead of relying on surface syntax.

**Serialization is not memory dumping.** In-memory layout can contain padding, native endianness, pointers, runtime headers, invalid/noncanonical bit patterns, or secrets. A wire/file format needs explicit field encoding, byte order, sizes, version, integrity limits, and validation. An array of integers serialized little-endian is a deliberate representation distinct from “whatever bytes this host uses.” Decode only after checking byte count, element count, multiplication overflow, and resource limits.

**Cost depends on the operation and regime.** Index address calculation is $O(1)$ in the abstract RAM model. Reading/writing includes bounds policy, element semantics, and memory-system behavior. Full traversal is $\Theta(n)$; linear search is $O(n)$; inserting/removing while preserving sequence order requires shifting $\Theta(n)$ elements or leaving a hole/side metadata because extent cannot grow or shrink. Copy is $\Theta(n)$ in element operations even when a bulk primitive lowers constants.

Contiguity often enables prefetching, vectorization, compact metadata, and few allocations, but never guarantees that one implementation wins. Element size, alignment, cache state, stride, working set, branch behavior, compiler, runtime, NUMA, device memory, and surrounding work can reverse rankings. Use [DSE-010](010-benchmarking-a-structure-without-misleading-results.md)'s evidence protocol rather than inherited ratios or a single timing.

**Concurrency is per memory location and contract.** Fixed extent prevents structural resizing but does not make concurrent element access safe. Unsynchronized conflicting accesses can be data races. Independent indices can still share cache lines and suffer false sharing; elements can point to shared mutable objects; a view can overlap. Partitioning by disjoint ranges supports parallelism only when ownership, element effects, aliasing, and memory ordering permit it. Publication of a fully initialized array also needs the language's visibility/synchronization guarantees.

**Security review follows the arithmetic and lifecycle.** Validate attacker-controlled extents before allocation; cap dimensions, total bytes, nesting, and work; reject truncated encodings; avoid speculative use of unchecked indices where threat models require mitigations; clear sensitive contents under a method the compiler/runtime contract preserves when required; and do not leak uninitialized/padding bytes. Memory-safe languages reduce classes of corruption but do not prevent resource exhaustion, stale logical data, index confusion, side channels, or unsafe FFI defects.

The following standard-library-only example implements a bounded $2\times3$ signed-32-bit matrix over an explicitly little-endian byte buffer. The byte order is a pedagogical storage/wire choice, not a claim about native array ABI.

<!-- bijux-verify: {"id":"checked-fixed-matrix-layout","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"shape=2x3\nstrides_bytes=(12, 4)\nflat=(10, 20, 30, 40, 50, 60)\nat_1_2=60\noffset_1_2=20\nbounds=IndexError\nbytes=24\nevidence=finite_checked_layout_trace\n","stderr":""}} -->
```python
class FixedInt32Matrix:
    item_size = 4

    def __init__(self, rows, columns):
        if not (0 <= rows <= 1_000 and 0 <= columns <= 1_000):
            raise ValueError("shape outside educational limit")
        cells = rows * columns
        if cells > 1_000_000:
            raise ValueError("matrix outside educational limit")
        self.rows = rows
        self.columns = columns
        self.storage = bytearray(cells * self.item_size)

    def offset(self, row, column):
        if not (0 <= row < self.rows and 0 <= column < self.columns):
            raise IndexError("matrix index out of bounds")
        return (row * self.columns + column) * self.item_size

    def set(self, row, column, value):
        offset = self.offset(row, column)
        self.storage[offset : offset + self.item_size] = value.to_bytes(
            self.item_size, "little", signed=True
        )

    def get(self, row, column):
        offset = self.offset(row, column)
        return int.from_bytes(
            self.storage[offset : offset + self.item_size], "little", signed=True
        )

    def flat_values(self):
        return tuple(
            self.get(row, column)
            for row in range(self.rows)
            for column in range(self.columns)
        )


matrix = FixedInt32Matrix(2, 3)
for index, value in enumerate((10, 20, 30, 40, 50, 60)):
    matrix.set(index // 3, index % 3, value)

print(f"shape={matrix.rows}x{matrix.columns}")
print(f"strides_bytes=({matrix.columns * matrix.item_size}, {matrix.item_size})")
print(f"flat={matrix.flat_values()}")
print(f"at_1_2={matrix.get(1, 2)}")
print(f"offset_1_2={matrix.offset(1, 2)}")
try:
    matrix.get(2, 0)
except IndexError:
    print("bounds=IndexError")
print(f"bytes={len(matrix.storage)}")
print("evidence=finite_checked_layout_trace")
```

This finite trace verifies the educational class's declared shape, row-major mapping, explicit encoding, and one rejected boundary case. It does not validate native C/Rust/Java/Go layout, compiler optimizations, pointer provenance, unsafe access, concurrency, FFI, or performance.

## Definitions and Notation

Let $T$ be an element type, $n\in\mathbb{N}$ an extent, and $A\in T^n$ an abstract fixed array. Let $B$ be a representation base, $s=size(T)$ the element-slot size under a stated layout, and $[0,n)=\{i\mid0\le i<n\}$ the valid index set.

For dimension vector $N=(n_0,\ldots,n_{d-1})$, logical index $I=(i_0,\ldots,i_{d-1})$ is valid when $0\le i_k<n_k$ for every $k$. Stride vector $S=(t_0,\ldots,t_{d-1})$ maps it to byte offset $o+I\cdot S$. **Dense row-major** and **dense column-major** are particular stride choices. A **ragged array** is a sequence of row arrays whose extents may differ.

An element is **initialized/live** after its construction contract succeeds and before destruction. A **view** is a non-owning or shared-ownership logical mapping to storage, depending on the API. **Provenance** denotes the language/IR constraints that tie a pointer and derived addresses to an allocated object; integer equality alone may not establish valid access.

## Mechanisms, Invariants, or Proof Structure

For one dimension, injectivity follows from positive $s$: if $i\ne j$, then $is\ne js$ in mathematical integers. Under overflow-free address arithmetic and an allocation of $ns$ bytes, each valid $i$ maps into `[B,B+ns)` and distinct indices map to distinct slot starts. This proof does not authorize language-level pointer formation unless alignment, provenance, lifetime, and type-access rules also hold.

For dense row-major $R\times C$, flattening $f(r,c)=rC+c$ maps valid indices into `[0,RC)`. If `f(r,c)=f(r',c')`, division with remainder by positive $C$ yields $r=r'$ and $c=c'$, so the mapping is injective. Empty dimensions require separate handling because division by zero is invalid even though the total element set is empty.

Partial construction uses invariant `live = [0,k)` for a prefix strategy: slots below $k$ contain valid `T`, slots at or above $k$ are raw storage, and failure cleanup destroys exactly `[0,k)` in the required order. Arbitrary initialization order needs a bitmap or equivalent ownership state rather than one counter.

## Alternatives and Trade-Offs

- **Fixed inline array** embeds predictable storage and extent; a dynamic array adds capacity/reallocation but supports growth.
- **Checked indexing** contains invalid access; unchecked indexing can reduce redundant checks only with a maintained proof obligation.
- **Extent in the type** enables compile-time constraints and specialization; runtime extent reduces type proliferation and supports dynamic inputs.
- **Value arrays** can give compact inline semantics; reference arrays support polymorphic objects but add indirection, nullability, and aliasing.
- **Owning copies** isolate mutation and lifetime; views avoid copying but add alias, validity, and stride obligations.
- **Dense multidimensional storage** gives simple strides; ragged rows support unequal lengths and independent allocation.
- **Row-major versus column-major** favors different traversal orders; neither is globally superior.
- **Structure of arrays versus array of structures** changes field locality, vectorization, and API ergonomics; measure the target workload.
- **Sentinel termination** saves a separate length in narrow domains; explicit extent supports arbitrary element values and bounded validation.
- **Native layout exchange** can be fast inside one governed ABI; explicit serialization is more portable, versionable, and defensible.

## Failure Modes and Misconceptions

1. **“Fixed means immutable.”** Extent is fixed; element mutation is a separate policy.
2. **“Fixed arrays live on the stack.”** Placement follows ownership, escape, embedding, allocation, runtime, and compiler rules.
3. **“Array access is always O(1), so all accesses cost the same.”** Address work is constant in the model; memory-system latency varies.
4. **“Contiguous always beats linked.”** Workload, size, mutation, compiler, and environment determine measured outcomes.
5. **“The pointer remembers length.”** Raw pointers ordinarily need an accompanying extent or stronger type.
6. **“One-past is an element.”** It may be a legal position but is not dereferenceable.
7. **“A bounds check alone makes access safe.”** Arithmetic, allocation, initialization, lifetime, alignment, provenance, aliasing, and synchronization also matter.
8. **“Zeroing initializes every type.”** Only types/languages with that representation guarantee permit it.
9. **“Copying bytes copies values.”** Resource ownership, pointers, padding, and nontrivial element operations can invalidate that assumption.
10. **“Nested arrays are rectangular and contiguous.”** Some are ragged reference graphs; verify the specific type/layout.
11. **“Transpose rearranges bytes.”** A view can transpose by changing shape/strides while sharing bytes.
12. **“Fixed extent makes concurrency safe.”** Element races, aliases, publication, and false sharing remain.
13. **“Native memory is a file format.”** ABI, padding, byte order, pointers, and versions make raw dumps nonportable or unsafe.
14. **“Memory-safe arrays eliminate security risk.”** Exhaustion, logic errors, stale views through unsafe boundaries, side channels, and FFI remain.

## Worked Examples

### Example 1

For `T[8]` with 4-byte contiguous slots, index 7 maps to offset 28 and its slot occupies bytes 28–31 within 32 element bytes. Index 8 is one-past as a position in contracts that support it, but reading it is invalid.

### Example 2

An attacker supplies dimensions `65536 x 65536` for 4-byte cells. Multiplication needs 17,179,869,184 bytes; 32-bit arithmetic can wrap. Check dimensions, product, byte size, policy limits, and allocation result before decoding any cells.

### Example 3

A C function parameter written with array syntax commonly adjusts to a pointer type. Passing `sizeof` inside the function reports pointer size, not caller-array bytes. Use an explicit count or extent-preserving wrapper and validate the pair.

### Example 4

A Rust `[Record; 16]` can be boxed, proving fixed extent does not imply stack placement. Safe indexing checks bounds; converting to a slice borrows the same elements with runtime length while the owner remains responsible for storage.

### Example 5

A Java `Dog[]` assigned to `Animal[]` still has runtime component type `Dog`. Attempting to store a `Cat` is dynamically rejected. The example distinguishes reference-array covariance from immutable read-only covariance.

### Example 6

A Java `int[][]` can have rows of lengths 2 and 5, so `(r,c)` validation must check the selected row and its length. It cannot be passed as a dense `R*C` integer buffer without conversion.

### Example 7

A `3x4` row-major `float64` matrix has strides `(32,8)` bytes. Its transpose view can use shape `(4,3)` and strides `(8,32)` while sharing storage; code demanding contiguous rows must copy or reject it.

### Example 8

Constructing an array of ten resource owners fails on the fourth construction. With prefix-live invariant `k=3`, cleanup destroys exactly elements 0–2 in the specified reverse or language-defined order and never touches raw slots 3–9 as objects.

### Example 9

Two threads update adjacent 8-byte counters in one array. Even when indices are distinct and language synchronization prevents races, both slots may occupy one cache line and contend. Padding/partitioning is a measured optimization, not a semantic requirement.

### Example 10

A fixed table of medication dosage limits uses explicit unit-tagged values and checked indices. Array mechanics can enforce extent and bounds, but clinical correctness, unit conversions, patient-specific rules, versioning, auditability, safety, and regulatory approval require named domain controls.

## Cross-Program Connections

- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns raw storage, lifetimes, unsafe access, ABI, and FFI discipline.
- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains type identity, exceptions, covariance, undefined behavior, and observational equivalence.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) explains bounds-check elimination, address IR, alias analysis, vectorization, and optimization assumptions.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, pages, protection, mapping, and allocation mechanisms.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache lines, prefetching, alignment, SIMD, NUMA, and false sharing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns integer-overflow, memory-corruption, exhaustion, information-leak, and unsafe-boundary threat models.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns sanitizer, property, fuzz, regression, portability, and evidence strategies.

## References

1. Rust Project, [The Rust Reference: Array Types](https://doc.rust-lang.org/reference/types/array.html). Fixed-size `[T; N]`, constant extent, initialization, bounds checking, and boxed arrays.
2. Rust Project, [The Rust Reference: Type Layout](https://doc.rust-lang.org/reference/type-layout.html#array-layout). Array size, alignment, element offsets, and slice layout.
3. ISO C++ working draft, [Arrays](https://eel.is/c++draft/dcl.array). Built-in array declarators, element type, bounds, multidimensional nesting, and contiguity wording.
4. ISO C++ working draft, [`std::array` Overview](https://eel.is/c++draft/array.overview). Extent-bearing aggregate container and checked/unchecked access surface.
5. Oracle, [Java Language Specification, Chapter 10: Arrays](https://docs.oracle.com/javase/specs/jls/se25/html/jls-10.html). Runtime length, array objects, nested/reference arrays, checked indexing, covariance, and store exceptions.
6. Go Project, [Go Language Specification: Array Types and Slice Types](https://go.dev/ref/spec#Array_types). Extent in array type, valid indices, nested arrays, zero values, copying, and slice descriptors.
7. ISO/IEC JTC 1/SC 22/WG14, [N3096: C23 Working Draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf). C array types, declarator adjustment, pointer arithmetic, object representation, initialization, and undefined behavior.
8. LLVM Project, [The Often Misunderstood GEP Instruction](https://llvm.org/docs/GetElementPtr.html). Address computation, object bounds, `inbounds`, negative indices, overflow, and dereference separation.
9. NumPy Project, [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Homogeneous fixed-size items, shape, byte order, buffers, offsets, strides, and row/column-major order.
10. NumPy Project, [Internal Organization of NumPy Arrays](https://numpy.org/doc/stable/dev/internals.html). Data buffers, metadata, shared views, shape, offset, byte order, and strides.
11. ISO/IEC JTC 1/SC 22/WG14, [N2889: Pointers and Integer Types](https://open-std.org/jtc1/sc22/wg14/www/docs/n2889.htm). Limits of deriving alignment and pointer properties from integer bit patterns.

## Exercises

### Exercise 1

Specify a generic fixed array of extent $N$, including abstraction, layout, construction, indexing, copying/moving, destruction, and zero extent.

### Exercise 2

Derive and prove a checked row-major offset function for a 3-D array, including overflow, empty dimensions, and allocation-size conditions.

### Exercise 3

Compare built-in C arrays, C++ `std::array`, Rust arrays, Java arrays, and Go arrays across extent typing, placement, bounds, initialization, copying, and views.

### Exercise 4

Design an FFI descriptor for a possibly strided two-dimensional array and state validation, ownership, mutability, concurrency, and serialization requirements.

### Exercise 5

Prepare a verification plan for a fixed array used in a safety-critical lookup table. Separate automated evidence from required domain and organizational review.

## Answers to the Exercises

### Answer 1

Model the value as $T^N$ with fixed type- or value-level extent under the chosen language. For contiguous inline layout require checked `N*size(T)`, correct alignment, and slot `i` at `B+i*size(T)`. Construction establishes all-live state; a raw-storage implementation tracks a live prefix/bitmap and cleans exactly constructed elements on failure. Checked access accepts `[0,N)`; unchecked access requires an explicit proof. Copy/move/destruction apply element operations under stated ordering and exception rules, never assumed bytewise. Zero extent has no valid element, so `front/back/index` fail and pointer identity is not assumed beyond specification. Storage placement and element mutability remain separate policies.

### Answer 2

For shape `(X,Y,Z)` and slot size `s`, validate each index, then compute flat index `((x*Y)+y)*Z+z` with checked multiply/add, or validate total and use checked strides `(Y*Z*s,Z*s,s)`. Prove by repeated quotient/remainder that valid triples map injectively into `[0,XYZ)`, and show maximum maps to `XYZ-1` when all extents are positive. Check `X*Y`, then `X*Y*Z`, then bytes times `s` before allocation. If any dimension is zero, the logical set is empty and access always rejects; do not use a proof step dividing by a zero extent.

### Answer 3

C built-in declarations carry bounds but many expressions/parameters adjust to pointers; whole arrays are not directly assignable and unchecked invalid access can be undefined. `std::array<T,N>` retains `N` in the type, is an aggregate/container, offers `at` and `operator[]`, and follows element operations. Rust `[T;N]` includes extent, requires initialized elements, uses safe checked indexing, and follows move/copy/borrow rules; it can be inline or boxed. Java `T[]` is a dynamically created object whose runtime length is not in the type; variables alias it, access is checked, components are initialized, and reference arrays are covariant with store checks. Go `[N]T` includes extent, initializes to zero values, bounds-checks/panics according to the spec, and array assignment copies values; slices are descriptors over underlying arrays. Exact ABI and optimization claims require their own specifications.

### Answer 4

Use descriptor fields for data pointer/handle, element type/encoding, item size, shape `(rows,cols)`, signed byte strides, base offset, total accessible allocation bytes, address space/device, alignment, ownership/release callback, lifetime token, mutability, and version. Validate nonnegative shape, checked products and extremal offsets, alignment, pointer/handle provenance as available, supported element encoding, and whether overlaps are allowed. Define who retains/releases storage, whether callbacks may fail, and how asynchronous users extend lifetime. Concurrent mutation needs disjointness or synchronization. For persistence/network exchange, serialize explicit values and metadata with byte order, version, limits, and integrity—not native pointers or headers.

### Answer 5

Review the abstract mapping, valid index domain, units, sentinel policy, update/version policy, initialization, storage/ABI, bounds, overflow, lifetime, and failure response. Use compile-time extent checks where available, static analysis, sanitizers/unsafe interpreters, boundary/property/model tests, malformed-input fuzzing, fault injection, cross-build/architecture tests, checksums/versioned deployment, and target-environment timing only for stated deadlines. Retain source/toolchain/configuration/results. Domain experts validate every table value and unit; safety engineers analyze hazards and failure containment; security, quality, operations, human-factors, accessibility, and regulatory owners review their scopes. Automated array evidence does not establish domain correctness, system safety, certification, or deployment fitness.
