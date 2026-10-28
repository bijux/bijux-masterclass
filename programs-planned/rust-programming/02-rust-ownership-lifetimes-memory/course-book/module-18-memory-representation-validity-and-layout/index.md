# 18 — Memory Representation, Validity, and Layout

**Course 2, day 8 · Module 18 of 90**  
`██████░░░░░░░░░░░░░░` **18/90**

[← Module 17: Interior Mutability and Runtime Borrows](../module-17-interior-mutability-and-runtime-borrows/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 19: Subtyping, Variance, PhantomData, and Drop Checking →](../module-19-subtyping-variance-phantomdata-and-drop-checking/index.md)

## The question

> Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?

## Why this comes now

The previous modules described semantic ownership and access. Memory-sensitive design also needs a disciplined distinction among validity, layout guarantees, target observations, and implementation details. This module prevents folklore about stack, heap, padding, niches, and fat pointers from becoming unsafe assumptions later.

## What you will be able to do

- Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.
- Reason about size, alignment, padding, field non-overlap, repr(Rust), repr(C), and repr(transparent) without overclaiming offsets.
- Explain thin and wide pointers, metadata, slices, str, trait-object previews, and unsized tails.
- Classify enum discriminant and niche claims by documented guarantees rather than pattern extrapolation.
- Build memory reports that distinguish inline size, length, capacity, shared allocation deduplication, allocator overhead, and exclusions.

## Core model

### Five levels of truth

Memory reasoning fails when distinct claims are collapsed. Classify every statement:

1. **semantic value:** what the program means;
2. **validity invariant:** which bit patterns/values are valid for a type;
3. **language/layout guarantee:** what Rust specifies about size, alignment, field non-overlap, or representation;
4. **library/platform contract:** what an API or target promises;
5. **observation:** what this compiler/target/build measured today.

An observation can guide investigation. It cannot become a portable serialization format or safety proof without a documented guarantee.

### Size, alignment, padding

`size_of::<T>()` reports the inline size of `T`, including padding. It does not include heap allocations owned by a `String`, `Vec`, `Box`, `Rc`, or map. `align_of::<T>()` reports alignment. `size_of_val` uses metadata for dynamically sized pointees.

For `repr(Rust)`, the compiler guarantees enough for safe field access and non-overlap but may choose field order and padding. Do not compute persistent offsets from source order. `repr(C)` provides a C-compatible layout algorithm for FFI purposes under its rules; it is not a complete cross-platform serialization format. `repr(transparent)` gives a single non-zero-sized field's layout/ABI relationship under documented constraints.

### Pointers and metadata

A reference to sized `T` is normally represented as a data pointer. A reference to `[T]` or `str` carries metadata such as length. A trait object carries metadata enabling dynamic dispatch. The course may observe word counts on a target, but public code should rely on documented pointer/metadata semantics rather than hard-coded byte sizes unless the target is explicit.

Owners and pointers have different accounting:

- `String`: inline handle plus separate buffer capacity;
- `Vec<T>`: inline handle plus element allocation;
- `Box<T>`: inline pointer plus allocation for `T`;
- `Rc<T>`: handle plus allocation including reference-count metadata and `T`;
- `&T`: borrowed pointer, no ownership of referent allocation.

### Enums and niches

The compiler may use invalid bit patterns (“niches”) of payload types to encode enum discriminants. Some optimizations are documented for specific types/cases; many observed layouts are not universal. Do not extrapolate “Option of anything pointer-like is always pointer-sized.” Even when size equality is guaranteed, byte encoding, padding, endianness, and version compatibility may not be.

A protocol should encode fields and discriminants explicitly.

### Validity is stronger than size

Two types with equal size are not interchangeable. Creating an invalid `bool`, reference, enum discriminant, or UTF-8 `str` can be undefined behavior in unsafe contexts. Safe code normally protects these invariants. Course 6/10 later study unsafe construction; here the rule is to reject transmute-style reasoning from size alone.

### Honest memory reporting

A report should define formulas:

```text
live text payload = Σ String::len(text)
live string capacity = Σ title.capacity + text.capacity + tag capacities
cached line descriptors = count of stored Range<usize>
unique snapshot payload = deduplicated snapshots by allocation identity
```

Then list exclusions:

- allocator headers and fragmentation;
- vector/map bucket capacity unless measured separately;
- `Rc` control block overhead unless specifically modeled;
- stack frames, code, runtime, and OS pages;
- transient allocations during report construction;
- shared allocations outside the workspace ownership graph.

Call the output a scoped accounting report, not total memory usage.

### Layout observatory discipline

Every measurement record includes:

```text
rustc -Vv:
target triple:
pointer width:
build profile:
type/expression:
measured value:
claim class: guarantee | library/target | observation
source or justification:
```

Tests for observations should not assert universal numeric values. They can assert relationships guaranteed by the contract, or record snapshots keyed by target when the course explicitly studies change.

### Derive it yourself

A team proposes writing `Option<Handle>` bytes to disk because `size_of` matches `Handle` on their machine. Classify every assumption, list missing encoding choices, and design a versioned explicit codec.

### Misconception clinic

- `size_of` is inline representation size, not transitive memory usage.
- `repr(Rust)` does not promise source field order.
- a niche observation is not automatically a stable ABI/format.
- padding is not application payload and may not contain initialized deterministic bytes.

Every layout statement belongs to one of three levels.

### 1. Semantic guarantee

The language/API guarantees ownership, valid operations, destruction, and observable behavior. Example: a `Vec<T>` owns its elements and preserves their sequence order.

### 2. Representation guarantee

The Reference or standard-library contract guarantees a layout property for a representation or type. Examples include `repr(C)` field layout rules, `repr(transparent)` constraints, and specified null-pointer optimizations for particular pointer-like types.

### 3. Observation

A particular compiler version, target, optimization level, and type combination yields a size, alignment, field address order, or generated code. `size_of::<T>()` is authoritative for that build, not automatically portable policy.

### Guarantee ledger

For every experiment, record:

| claim | level | target/toolchain | safe dependency? |
|---|---|---|---|
| `size_of::<&u8>() == 8` | observation on 64-bit target | named environment | no portable API dependency |
| fields do not overlap | Rust representation guarantee | language | yes |
| `Box<T>` drops `T` | semantic/API guarantee | standard library | yes |

### Why this discipline matters

Layout folklore causes:

- persisted files that break after compiler/target changes;
- FFI structures with wrong field representation;
- unsafe code assuming padding bytes are initialized;
- enum tags decoded from observed memory;
- performance arguments based on one debug build.

This course remains safe, but safe code can still make wrong product assumptions from layout observations.

### Observation tools

Use:

```rust
std::mem::size_of::<T>()
std::mem::align_of::<T>()
std::mem::size_of_val(&value)
std::mem::align_of_val(&value)
```

Field addresses can be observed through references converted for display, but do not dereference reconstructed raw pointers. Miri and compiler layout diagnostics belong to later unsafe/performance courses.

### Write claims narrowly

Prefer:

> On the course's 64-bit target and Rust 1.97.1, this build observes a two-word slice reference.

over:

> Rust references are always 16 bytes.

The first is evidence; the second is false generalization.

**Size** is the byte stride required for values in an array of `T`. **Alignment** is the address divisibility requirement for valid placement of `T`. Padding may be inserted so fields and the whole type meet alignment constraints.

### Simple `repr(C)` calculation

```rust
#[repr(C)]
struct Header {
    kind: u8,
    length: u32,
    flags: u16,
}
```

Under a target where alignments are 1, 4, and 2:

- `kind` at offset 0;
- three padding bytes before `length` at offset 4;
- `flags` at offset 8;
- tail padding to make total size a multiple of max alignment 4, giving size 12.

This calculation depends on `repr(C)` rules and target type alignments.

### `repr(Rust)` restraint

The default representation guarantees fields are properly aligned, non-overlapping, and the type alignment is at least each field's. It does not promise source declaration order as physical field order. The compiler may reorder fields to reduce padding.

Therefore, do not write default-layout offset assertions as portable course requirements.

### Arrays

`[T; N]` stores `N` contiguous `T` values with stride `size_of::<T>()`. Total size is `size_of::<T>() * N` when representable. This is stronger than arbitrary struct-field layout.

### References and padding bytes

Safe value assignment does not promise meaningful contents in padding. Padding should not be hashed, serialized, compared, or exposed as initialized payload by copying raw object bytes.

### Alignment and allocation

Heap allocation does not remove alignment requirements. Allocators return storage suitable for requested layout. A pointer into a byte buffer may not be aligned for a larger type, which is one reason reinterpreting bytes belongs to unsafe code with explicit validation.

### Optimization is not semantic packing

A smaller struct can improve cache density, but field reordering for size should follow measurement and public-representation constraints. Readability and logical grouping often dominate until Course 9 profiling shows a real hot structure.

Representation attributes alter or constrain layout. They are not general performance decorations.

### `repr(C)`

`#[repr(C)]` uses C-compatible field-order/alignment rules for structs and specified enum representation behavior. It is appropriate for FFI boundaries and stable layout calculations within documented target ABI assumptions.

It does not make every field FFI-safe. `String`, `Vec`, Rust references, and many enums have no C ABI representation merely because the outer struct is `repr(C)`.

### `repr(transparent)`

A transparent wrapper has the same layout and ABI as its single non-zero-sized field, subject to attribute rules:

```rust
#[repr(transparent)]
struct DocumentId(u64);
```

This is useful for FFI/newtype representation and makes the wrapper's layout relation explicit. It does not automatically define serialization byte order or validation semantics.

### Integer representation for fieldless enums

```rust
#[repr(u8)]
enum Status {
    Ready = 1,
    Done = 2,
}
```

This constrains discriminant representation for appropriate enums. Reading arbitrary `u8` as `Status` is still invalid when the byte is not a declared discriminant.

### `repr(packed)`

Packed representations reduce alignment/padding and can create unaligned fields. Taking references to unaligned fields is hazardous and often rejected. This course does not use packed structs; systems programming will cover byte-wise access and unsafe constraints.

### `repr(align(N))`

Explicit alignment can support hardware/cache/ABI requirements but increases size/spacing. It is not a generic speed switch.

### Combinations and portability

Representation attributes interact with target ABI. A stable on-disk format still needs explicit field encoding, endianness, versioning, and validation.

### Capstone rule

Generational handles may use `repr(transparent)` newtypes for clarity, but persistence never writes their in-memory bytes directly. The memory report labels representation observations rather than promising ABI.

Pointers to sized values need enough information to locate a value whose size is statically known. Pointers to DSTs need metadata.

### Slice reference

A `&[T]` conceptually contains a data address and element length. `size_of_val(slice)` computes `length * size_of::<T>()`, not the size of the reference handle.

```rust
let values: &[u16] = &[10, 20, 30];
assert_eq!(std::mem::size_of_val(values), 6);
```

### `str`

A `&str` carries byte length. `size_of_val(text)` is UTF-8 byte count, not character count.

### Trait-object metadata

A `&dyn Trait` carries metadata for dynamic dispatch and layout of the erased concrete value. Exact metadata representation is not a public serialization format. Course 3 develops trait objects; here, understand why the pointer is observed as wide.

### Boxed DSTs

`Box<[T]>` and `Box<str>` are owning wide pointers. The allocation size is determined by metadata. The box handle's observed size differs from the pointee's dynamic size.

### Null and niches

References are non-null when valid. This can allow `Option<&T>` to use a null representation for `None` under documented guarantees. Do not extrapolate every observed equal-size `Option<T>` to a guaranteed niche optimization.

### Pointer address is not full validity

A valid pointer also involves alignment, provenance/association with an allocation, metadata, and the referent's validity. Printing an address is not enough to reconstruct a reference. The course never creates references from integers.

### `size_of_val` for trait objects

It reports the dynamic concrete size through metadata. This can aid diagnostics, but branch logic based on hidden concrete size often indicates an abstraction leak.

A memory report should separate the size of an owner value from the storage it controls.

### `String`

A `String` value stores control information for an owned UTF-8 buffer, commonly pointer, length, and capacity in some order. The exact field order is not a public contract. `size_of::<String>()` measures the control value, not allocated capacity.

### `Vec<T>`

Similarly, a `Vec<T>` controls an allocation with length and capacity. `size_of::<Vec<T>>()` remains constant across element counts, while heap allocation changes.

### `Box<T>`

For sized `T`, the box owner is typically pointer-sized; the allocation holds `T`. For DSTs, the box is wide. `size_of::<Box<T>>()` does not include pointee size.

### `Rc<T>`

The `Rc` handle is pointer-like. The allocation contains `T` and reference-count bookkeeping. Exact overhead is implementation detail. Strong/weak liveness behavior is guaranteed; byte layout is not.

### Inline containers

Arrays and small structs store contents inline. Moving them semantically moves the complete value, though optimization may eliminate physical copies.

### Capacity is policy state

Two equal strings can have different capacities. Capacity affects future allocation behavior but not string equality. Snapshots using `Box<str>` discard growable capacity as part of phase conversion.

### Memory accounting caveats

Accurate total memory includes allocator overhead, shared allocations counted once, spare capacity, recursive graph traversal, and interned/shared data. A simple `size_of` report is an educational approximation, not production heap profiling.

### Capstone report

The capstone memory report must label:

- inline control bytes observed;
- logical payload bytes;
- allocated capacity where APIs expose it;
- shared snapshot payload counted once by allocation identity within the process;
- approximations and exclusions.

An enum must represent which variant is active plus that variant's payload. The compiler may use unused bit patterns—niches—in payload types to encode the variant without adding a separate tag.

### Null pointer optimization

Valid references and certain nonzero pointer-like types cannot be null. `Option<&T>` can therefore represent `None` using null while using valid pointer representations for `Some`. The standard library documents guarantees for specific types.

### Do not generalize from size equality

You may observe:

```rust
size_of::<Option<SomeType>>() == size_of::<SomeType>()
```

That observation does not automatically guarantee the encoding or future equality for arbitrary types. Record whether a documented guarantee exists.

### Payload size

An enum's observed size is influenced by largest payload, alignment, discriminant strategy, and available niches. Boxing a rare large payload may reduce inline enum size at allocation cost.

### Fieldless discriminants

`std::mem::discriminant` returns an opaque value suitable for equality/hash comparison of variants, not numeric serialization. Explicit `repr` and discriminant values can define numeric representation for supported enum forms, but validation remains required.

### Invalid bit patterns

Not every byte pattern is a valid Rust value. `bool`, references, enums, `char`, and nonzero integer types have validity constraints. Reading arbitrary bytes as these types through unsafe reinterpretation can be undefined behavior. The safe course uses parsing/constructors instead.

### Domain protocol

Persist enum variants through explicit textual or integer codes with versioning and unknown-value errors. Do not dump memory representation.

### Niche as optimization, not architecture

Do not distort domain types solely to chase one-byte savings without measuring hot-scale impact. Representation should first make invalid states unrepresentable and APIs clear.

A zero-sized type (ZST) has size zero, such as `()` and empty marker structs:

```rust
struct Validated;
assert_eq!(std::mem::size_of::<Validated>(), 0);
```

ZSTs can carry type-level meaning without per-value payload bytes.

### Marker states

A generic wrapper can encode a protocol state:

```rust
struct Draft;
struct Committed;

struct Record<State> {
    text: String,
    state: std::marker::PhantomData<State>,
}
```

Course 9 studies `PhantomData` semantics in depth. The marker type may be zero-sized, but the type distinction changes which methods compile.

### Collections of ZSTs

A `Vec<Zst>` can represent a logical length without allocating one byte per element. Its capacity behavior is special. Do not use element addresses as unique identities: distinct ZST values may have equal addresses because no storage is required.

### Alignment can be nontrivial

A zero-sized type may still have alignment greater than one under representation attributes. Size zero does not mean “irrelevant to layout.”

### Empty arrays and tuples

`[T; 0]` is zero-sized but retains `T` in its type. `()` is the unit value/type. These can influence generic behavior, trait implementations, and drop checking even without payload bytes.

### Marker ownership effects

A marker field can affect variance, drop checking, and auto-trait behavior despite zero runtime size. “Zero size” does not mean “zero semantic effect.” This distinction prepares Module 19.

### Address-sensitive code

Pinning and pointer identity should not rely on unique addresses for ZSTs. Address observations are especially misleading when no storage is needed.

A persisted format needs an explicit byte/text grammar independent of compiler layout.

### Why raw copying fails

- padding bytes may be unspecified or uninitialized;
- field order under `repr(Rust)` is not promised;
- endianness differs by target;
- pointers are process-local addresses, not content;
- `String`/`Vec` control blocks point elsewhere;
- enum encodings may change;
- type validity excludes arbitrary byte patterns;
- version evolution has no schema.

### Explicit encoding

Encode each logical field:

```text
version
identifier
revision
length-prefixed UTF-8 title
length-prefixed UTF-8 body
```

Choose byte order, integer width, length limits, and error behavior. Validate before constructing domain types.

### `repr(C)` is not a file format

Even a C-compatible struct reflects target ABI, endianness, and field-type definitions. It can support FFI with the matching ABI, not universal persistence.

### Hashing memory is equally flawed

Hash semantic fields through their `Hash` implementations or explicit encoding. Hashing object bytes includes padding and pointer addresses and can vary across runs.

### Capstone snapshots

Snapshots remain in memory for this course. If exported, use an explicit versioned format like Course 1's storage grammar. The memory-report command never emits reconstructible raw object bytes.

### Review question

Whenever code uses `size_of::<T>()` to allocate a serialization buffer, ask whether it is encoding a semantic value or copying an implementation representation. Only the former is an ordinary safe product format.

A team wants to compare representations of IDs, options, pointers, and snapshots. The observatory must teach without converting measurements into false contracts.

### Record schema

```text
type label
target/toolchain label
size_of
align_of
selected field offsets when safely observable
classification: guaranteed / library contract / observed
notes and excluded heap data
```

Do not serialize values or read padding. Obtain addresses of fields through references and subtract integer addresses only as an observation within one live value; do not dereference reconstructed pointers.

### Example claims

- “`u32` has size 4” is a primitive layout guarantee.
- “`String` is three words” is a common observation, not a public representation contract.
- “slice elements are contiguous” is a contract.
- “`Option<&T>` uses the null niche” has documented guarantees in specified cases; state exact scope.
- “our custom wrapper preserves the niche” needs `repr(transparent)` preconditions or remains observation.

### Inline/deep split

For `Rc<Snapshot>` report inline owner size separately from:

- control block: excluded/private;
- snapshot struct inline allocation;
- owned title/text/tag payload bytes;
- map buckets and allocator metadata: excluded;
- multiple aliases: deduplicated by allocation identity for one traversal.

### Protocol refusal

The observatory output must never become a persisted ABI by copying raw bytes. A portable protocol uses explicit fields, versions, widths, endian, validity checks, and semantic discriminants.

### `repr` experiment

Compare default, `repr(C)`, and `repr(transparent)` declarations. Explain expected guarantees before running. A test may assert `repr(transparent)` size/alignment equality when declaration satisfies the attribute, but not arbitrary field offsets for default layout.

### Niche experiment

Measure `Option<NonZeroU64>`, `Option<&u8>`, and `Option<CustomHandle>`. Label which equalities are guaranteed and which are observed. Add a field to the wrapper and observe possible change without presenting it as required.

### Performance boundary

A smaller owner may improve density, but no performance conclusion follows until Course 9 benchmarks realistic arrays/access patterns. The observatory establishes legal assumptions and hypotheses.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Produce a memory report with formulas, target observations, and explicit exclusions. Do not present `size_of` observations as a complete allocation or ABI account. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-08-layout-observatory/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 19 when you can:

- answer the module question—“Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Type layout](https://doc.rust-lang.org/reference/type-layout.html)
- [Rust Reference: Type validity](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

[← Module 17](../../../02-rust-ownership-lifetimes-memory/course-book/module-17-interior-mutability-and-runtime-borrows/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 19 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md)

## Continue

1. Complete the [Module 18 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 18 — Layout Observatory](../../labs/module-08-layout-observatory/README.md) from its public contract.
3. Apply the Module 18 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
