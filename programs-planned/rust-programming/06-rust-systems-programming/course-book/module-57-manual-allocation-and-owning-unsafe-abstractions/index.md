# 57 — Manual Allocation and Owning Unsafe Abstractions

**Course 6, day 7 · Module 57 of 60**  
`███████████████████░` **57/60**

[← Module 56: Raw Pointers, Provenance, and Uninitialized Memory](../module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) · [Course 6 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries →](../module-58-c-ffi-abi-strings-and-error-boundaries/index.md)

## The question

> How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?

## Why this comes now

Raw pointers become useful only when an abstraction owns their entire lifecycle. Module 57 assembles allocation, layout, initialization, and destruction into a small `AlignedBytes` type. It deliberately does not build a generic `Vec<T>` clone: generic growth, element moves, zero-sized types, variance, and panic safety are a larger proof surface. The point is to learn how to choose the smallest unsafe abstraction that solves a measured requirement.

## What you will be able to do

- Construct and validate `Layout` values without unchecked size arithmetic.
- Distinguish allocation capacity from initialized logical length.
- Handle zero-length allocations without passing an invalid layout to the allocator.
- Pair every successful allocation with exactly one matching deallocation layout.
- Design `Drop` and construction failure so no state leaks or double-frees.
- Review auto traits, variance, and reallocation before generalizing an owner.

## Core model

### The allocator contract begins with `Layout`

The global allocation functions operate on a `Layout`: a size and power-of-two alignment that satisfies additional bounds. Construct it through `Layout::from_size_align` or compositional methods rather than unchecked arithmetic.

```rust
let layout = std::alloc::Layout::from_size_align(length, alignment)
    .map_err(|_| AllocationError::InvalidLayout { length, alignment })?;
```

The layout is not metadata you may recompute approximately during drop. The exact allocation contract used for allocation must be available for deallocation. An owning type can store the `Layout` directly or store enough invariant-checked fields to reconstruct it exactly.

### Allocation returns raw storage, not initialized values

`alloc(layout)` returns a pointer to uninitialized bytes or null on failure. `alloc_zeroed` requests zero-filled bytes, which are valid for `u8` but not automatically valid for every `T`. The allocator does not create a Rust slice or transfer cleanup into RAII.

An owner must immediately establish a state that can be dropped safely on every later path. For `AlignedBytes`, zeroed bytes mean all `length` elements are initialized `u8`, so the safe slice methods can expose exactly that range. For a generic `T`, capacity and initialized length would need separate tracking.

### Zero length needs a separate representation

Raw allocation APIs have special requirements around zero-size layouts and historical allocator behavior. An owner does not need an allocation to represent an empty byte sequence. Use a well-aligned dangling pointer and skip deallocation:

```rust
if length == 0 {
    return Ok(Self {
        pointer: std::ptr::NonNull::dangling(),
        length: 0,
        layout: None,
    });
}
```

Every method must respect the same state distinction. Empty slices can be constructed from a non-null aligned dangling pointer because no byte is accessed. `Drop` deallocates only when a real layout exists.

### Null is allocation failure, not an empty buffer

After a nonzero allocation request, convert the result through `NonNull::new`. A null return means allocation failed. A library may return a typed error or invoke `handle_alloc_error`, which usually aborts according to the allocator failure policy. FrameVault returns an error from its buffer constructor so failure is explicit at the application boundary.

Do not silently replace allocation failure with an empty allocation. That changes data length and can cause later writes through a dangling pointer.

### One owner, one deallocation

The owning invariant for `AlignedBytes` is:

```text
length == 0:
    pointer is non-null and aligned but not dereferenced
    layout is None
length > 0:
    layout is Some(exact allocation layout)
    pointer identifies a live allocation of at least layout.size() bytes
    first length bytes are initialized
    this value owns the unique deallocation responsibility
```

Private fields prevent safe code from manufacturing a false state. The type does not implement `Copy` or `Clone` automatically. Moving the owner transfers fields and deallocation responsibility; Rust then drops only the moved-to value.

### Safe slice exposure binds access to the owner borrow

The conversion from raw storage to a slice is unsafe internally, but the public method is safe because the type invariant proves it:

```rust
pub fn as_slice(&self) -> &[u8] {
    // SAFETY: the invariant guarantees a live initialized byte range for
    // `length`; the returned lifetime is bounded by `&self`.
    unsafe { std::slice::from_raw_parts(self.pointer.as_ptr(), self.length) }
}

pub fn as_mut_slice(&mut self) -> &mut [u8] {
    // SAFETY: `&mut self` provides exclusive access to the owned range.
    unsafe { std::slice::from_raw_parts_mut(self.pointer.as_ptr(), self.length) }
}
```

The methods do not return a caller-chosen lifetime. Borrowing ties access to the owner and prevents deallocation or competing mutable access while the slice exists.

### Drop must reproduce the allocation contract exactly

`Drop` checks whether a real layout exists and calls `dealloc(pointer, layout)`. The pointer must be the one returned by the allocator for that layout and must not already have been deallocated.

For `u8`, there are no element destructors. A generic container would first drop every initialized element, then deallocate raw storage. If element dropping panics, the language and panic strategy complicate cleanup; standard containers use carefully audited patterns. This is one reason the course abstraction stays byte-specific.

### Reallocation is a different proof, not a small add-on

`realloc` can move the allocation. Every pointer and reference into the old allocation becomes invalid if movement occurs. The new layout, failure behavior, copy size, and ownership transfer need explicit rules. A null result from reallocation generally leaves the original allocation owned by the caller, so overwriting the only pointer before checking can leak memory.

FrameVault does not need growth. It obtains a validated final payload size, allocates once, and fills exactly that many bytes. Deleting an unnecessary feature is often the strongest unsafe-code improvement.

### Generic raw vectors multiply the proof surface

A `RawVec<T>`-like design must handle:

- zero-sized `T`;
- alignment of `T`;
- element-count to byte-size overflow;
- capacity constraints relative to `isize::MAX`;
- partially initialized elements;
- moving and dropping non-`Copy` values;
- variance and `PhantomData<T>`;
- `Send` and `Sync` behavior;
- panic during element construction or growth.

The standard library already provides `Vec<T>`. Reimplementing it is educational in a dedicated unsafe-code study, but shipping a weaker version merely to avoid one allocation policy is not justified.

### Alignment must come from a real consumer requirement

Over-aligned bytes can support platform APIs, direct I/O, SIMD staging, or foreign libraries. Alignment alone does not make typed casts safe or improve performance universally. FrameVault chooses a configurable alignment only to exercise an explicit allocation contract; the default application path can use ordinary `Vec<u8>` unless a caller requests the aligned reader.

Course 9 will measure performance. Course 6 requires a correctness reason and honest cost: manual allocation adds code and audit burden, so its use must remain narrow and replaceable.

### Auto traits are part of the public contract

Raw-pointer-containing types may not receive the `Send` and `Sync` behavior you expect. Adding unsafe implementations because “the allocation is just bytes” would require a concurrency proof about ownership and aliasing. That belongs to Course 7.

Course 6’s `AlignedBytes` makes no manual `Send` or `Sync` promises. This conservative choice keeps the current abstraction’s contract aligned with what has been proved.

### `AlignedBytes` reference design

The complete shape is intentionally small:

```rust
pub struct AlignedBytes {
    pointer: std::ptr::NonNull<u8>,
    length: usize,
    layout: Option<std::alloc::Layout>,
}
```

Construction:

```rust
pub fn new_zeroed(length: usize, alignment: usize)
    -> Result<Self, AllocationError>
{
    if length == 0 {
        if !alignment.is_power_of_two() {
            return Err(AllocationError::InvalidAlignment(alignment));
        }
        return Ok(Self {
            pointer: std::ptr::NonNull::dangling(),
            length: 0,
            layout: None,
        });
    }

    let layout = std::alloc::Layout::from_size_align(length, alignment)
        .map_err(|_| AllocationError::InvalidLayout { length, alignment })?;

    // SAFETY: `layout` is valid and nonzero. The returned storage is owned by
    // this constructor until committed to `Self` or deallocated on failure.
    let raw = unsafe { std::alloc::alloc_zeroed(layout) };
    let pointer = std::ptr::NonNull::new(raw)
        .ok_or(AllocationError::AllocationFailed { length, alignment })?;

    Ok(Self {
        pointer,
        length,
        layout: Some(layout),
    })
}
```

If the allocation fails and returns null, no allocation exists to clean up. Once `Self` is constructed, `Drop` is the sole cleanup owner.

```rust
impl Drop for AlignedBytes {
    fn drop(&mut self) {
        if let Some(layout) = self.layout {
            // SAFETY: the type invariant says this is the live pointer returned
            // for exactly `layout`, and this is its unique deallocation path.
            unsafe { std::alloc::dealloc(self.pointer.as_ptr(), layout) };
        }
    }
}
```

The design stores `Option<Layout>` rather than inferring real allocation from `length`; the state representation says explicitly whether allocation occurred.

### Reading into the owner

A safe helper accepts any `Read`:

```rust
pub fn read_exact_aligned<R: Read>(
    reader: &mut R,
    length: usize,
    alignment: usize,
) -> Result<AlignedBytes, ReadAlignedError> {
    let mut bytes = AlignedBytes::new_zeroed(length, alignment)?;
    reader.read_exact(bytes.as_mut_slice())?;
    Ok(bytes)
}
```

On read failure, `bytes` drops and deallocates. The returned owner contains initialized bytes because zero initialization happened before the read; partial read failure does not expose a false initialized length. This is a deliberate simplification. An uninitialized allocation could avoid zeroing, but then `Read` cannot safely receive a `&mut [u8]` until initialization is represented through `MaybeUninit`-aware APIs. The small extra write buys a much smaller proof.

### Why not cast the aligned bytes

Even with 64-byte alignment, `as_slice().as_ptr() as *const Header` is not automatically a valid `Header`. The byte sequence may violate field validity, padding may be uninitialized under a different construction, the file is little-endian, and the lifetime/aliasing relation must still be proved. Alignment solves one condition only.

FrameVault keeps explicit decoding. The aligned owner demonstrates allocation discipline rather than serving as an excuse for layout-dependent parsing.

### Unsafe surface accounting

The reference implementation needs only three unsafe operations:

1. allocate zeroed storage;
2. construct borrowed slices from the owned pointer and length;
3. deallocate with the stored layout.

No raw arithmetic, reallocation, typed pointer cast, manual trait implementation, or partial element drop is required. This is the deletion test applied to unsafe code.

## Use the idea in a complete program

FrameVault adds `AlignedBytes`, a fixed-length zero-initialized byte owner with validated power-of-two alignment, explicit zero-length state, borrowed slice access, and exact deallocation. The file loader may choose it for staging an archive of known bounded size. The parser still receives an ordinary `&[u8]`, so unsafe storage does not leak into format logic.

The matching independent laboratory is [Aligned Byte Buffer](../../labs/module-07-aligned-byte-buffer/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) by drawing the allocation owner's zero, allocated, borrowed, moved, and dropped states. Build the Aligned Byte Buffer lab, test zero-sized and invalid-layout requests, and verify that FrameVault deallocates with the exact layout used for allocation without exposing raw ownership to callers.

## Ready to continue

You are ready when you can state the owner invariant for every constructor and destructor state, explain why a byte-specific fixed allocation is smaller than a generic vector, and show that every unsafe block follows from private fields and ordinary borrows.

## Primary Rust references

- [Rust standard library: alloc module](https://doc.rust-lang.org/std/alloc/index.html)
- [Rust standard library: Layout](https://doc.rust-lang.org/std/alloc/struct.Layout.html)
- [Rust standard library: alloc_zeroed](https://doc.rust-lang.org/std/alloc/fn.alloc_zeroed.html)
- [Rustonomicon: implementing Vec](https://doc.rust-lang.org/nomicon/vec/vec.html)

## Continue

1. Complete the [Module 57 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 57 — Aligned Byte Buffer](../../labs/module-07-aligned-byte-buffer/README.md) from its public contract.
3. Apply the Module 57 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
