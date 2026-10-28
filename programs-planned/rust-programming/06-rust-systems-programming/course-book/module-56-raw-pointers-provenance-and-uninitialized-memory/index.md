# Module 56 — Raw Pointers, Provenance, and Uninitialized Memory

**Course 6 · Day 6 · Module 56 of 100**
`██████████████░░░░░░░░░░░` **56/100**

[Program](../../../README.md) · [Course 6](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-06-panic-safe-batch-builder/README.md) · [FrameVault guide](../capstone.md)

[← Module 55: Unsafe Rust as a Proof Boundary](../module-55-unsafe-rust-and-safety-proofs/index.md) · [Module 57: Manual Allocation and Owning Unsafe Abstractions →](../module-57-manual-allocation-and-owning-unsafe-abstractions/index.md)

## The question

> How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

## Why this comes now

Module 55 established the proof method. This module supplies the raw operations that require it. The aim is not to memorize pointer methods. It is to track allocation identity, byte range, alignment, initialization state, aliasing permission, and lifetime as separate dimensions. Conservative reasoning is preferred where the formal memory model remains subtle.

### Prerequisite bridge

Module 55 established **Unsafe Rust as a Proof Boundary**. Before continuing, verify that you can review unsafe code through explicit claims rather than intuition or successful tests. This module preserves that capability and adds the ability to distinguish raw pointers from references and explain why conversion does not transfer ownership. Module 57, **Manual Allocation and Owning Unsafe Abstractions**, will rely on both when it asks: *How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?*

### Scope boundary

This module owns the reasoning for **raw pointers, provenance, and uninitialized memory** inside Course 6. The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Distinguish raw pointers from references and explain why conversion does not transfer ownership.
- Use raw borrow operators when creating a reference would itself be invalid.
- Derive pointer arithmetic from one allocation and checked element counts.
- Use `MaybeUninit` to represent storage that is not yet a valid `T`.
- Construct and clean up partially initialized sequences without leaks or invalid drops.
- Use `NonNull` as a non-null raw pointer component, not as proof of validity or ownership.

## Core model

### Raw pointers carry fewer enforced guarantees

`*const T` and `*mut T` may be null, dangling, misaligned, or point to uninitialized data. Creating or copying the pointer is usually permitted. Dereferencing it, converting it to a reference, reading, writing, or performing arithmetic imposes preconditions.

A raw pointer does not own its allocation. It does not keep the allocation alive. Its mutability marker does not by itself establish exclusive access. `*mut T` is a capability-shaped type, not a borrow checked by the compiler.

Track the owner separately. In FrameVault’s aligned buffer, the owner is the `AlignedBytes` value; the `NonNull<u8>` field identifies the allocation while length and layout describe it.

### Creating a reference can already be undefined behavior

References must be aligned, non-null, point to a valid value, and obey aliasing rules even if they are never dereferenced later. For packed fields or possibly invalid storage, do not write `&place as *const T`, because the intermediate reference may violate alignment or validity.

Use raw borrow syntax or address macros:

```rust
let pointer = &raw const packed.field;
// or
let pointer = std::ptr::addr_of!(packed.field);
```

Then use an operation matching the actual alignment contract, such as `read_unaligned`, rather than creating a reference.

### Pointer arithmetic is constrained by allocation identity

Methods such as `add`, `sub`, and `offset` are not integer arithmetic over the address space. The resulting pointer and traversed range must satisfy the method’s allocation and bounds contract. One-past-the-end pointers have limited uses but cannot be dereferenced.

Convert element counts to byte sizes with checked multiplication when allocating or validating external lengths. Do not derive a pointer into one allocation by arithmetic starting from an unrelated pointer merely because the numeric addresses happen to line up.

Provenance—the relationship between a pointer and the allocation or object from which it originated—is an evolving formal area. Portable code should preserve pointers through documented operations and avoid round-tripping through integers unless a specific API contract permits the intended use.

### Alignment is a property of the access

A byte buffer can begin at any alignment suitable for `u8`. Casting its address to `*const u32` does not make it aligned for `u32`. Even aligned bytes may not contain a valid `u32` representation in the desired endianness.

For binary parsing, copying exact bytes into an array and using `from_le_bytes` is clearer and safer. Raw typed loads belong where representation, alignment, and performance have been measured and documented. `read_unaligned` relaxes alignment only; it does not solve bounds, initialization, provenance, or aliasing.

### Read, write, and copy have different ownership effects

`ptr::read` copies bits out without marking the source uninitialized in the type system. Logically it transfers ownership of a non-`Copy` value; using or dropping the original afterward can double-drop. `ptr::write` places a value without dropping the old contents, so overwriting an initialized value can leak it.

`copy_nonoverlapping` corresponds to a non-overlapping memory copy; `copy` permits overlap like `memmove`. Both require valid ranges and initialized source bytes appropriate for the operation. They do not update collection lengths or ownership metadata.

The proof must match the exact operation, not the vague statement “both pointers are valid.”

### `MaybeUninit<T>` represents not-yet-a-value

Uninitialized memory is not a `T`. Many Rust types have invalid bit patterns: references cannot be null, `bool` has only two valid values, and enums have valid discriminants. Creating an uninitialized `T` is therefore wrong even if you plan to fill it immediately.

Use `MaybeUninit<T>`:

```rust
let mut slot = std::mem::MaybeUninit::<String>::uninit();
slot.write(String::from("ready"));
// SAFETY: `write` initialized the slot exactly once.
let value = unsafe { slot.assume_init() };
```

`MaybeUninit` suppresses automatic dropping because it does not claim to contain a live `T`. The caller must know exactly which slots are initialized.

### Partially initialized arrays need an initialized-prefix invariant

To build `[T; N]` when each element may fail or panic, allocate `[MaybeUninit<T>; N]` and maintain `initialized: usize`. After each successful write, increment the count. A guard drops only `0..initialized` on early exit.

The invariant is:

```text
slots[0..initialized] contain valid live T values
slots[initialized..N] are not treated as T
```

Only after all `N` writes succeed may the storage be converted to `[T; N]`. The conversion must not run the guard’s cleanup afterward. This is a compact example of panic safety and state transfer.

### `NonNull<T>` proves only non-nullness

`NonNull<T>` is useful in owning containers and optional-pointer optimizations. It is covariant over `T`, so generic mutable owners may need `PhantomData` choices to express ownership and variance correctly. It does not prove that the pointer is aligned, live, initialized, dereferenceable, uniquely owned, or allocated with any particular layout.

`NonNull::dangling()` provides a well-aligned non-null placeholder. It must never be dereferenced unless a real allocation exists. It is commonly used for zero-length owners whose methods avoid memory access.

### Raw slices still require a complete proof

`slice::from_raw_parts` and `from_raw_parts_mut` need more than a non-null pointer and a plausible length. The entire range must belong to one allocation, be aligned, initialized for `T`, fit within `isize::MAX` bytes under the API contract, and remain alive for the chosen lifetime. Mutable slices additionally require exclusive access.

The lifetime in the returned reference is inferred from surrounding use; the function cannot discover how long the allocation lives. Safe wrappers should tie the result to a real input borrow or keep construction private so callers cannot choose an arbitrary lifetime.

### Do not infer typed layout from network or file bytes

Even after learning raw loads, the correct parser for FrameVault remains Module 51’s explicit byte decoder. A file format is not a memory dump. Raw pointer operations are used for owned storage, FFI, and carefully defined layouts—not to erase format design.

This restraint is part of expertise: knowing an operation exists and recognizing when it weakens the contract.

### Model initialization as a state machine

For every raw storage algorithm, list states such as allocated-uninitialized, prefix-initialized, fully-initialized, moved-out, and deallocated. Define which destructor runs in each state and which transitions can panic.

If the algorithm cannot be explained as a finite state machine with one owner and one cleanup responsibility, the unsafe code is not ready.

### Complete initialized-prefix pattern

A fixed array builder can be written with a guard that always owns cleanup:

```rust
use std::mem::MaybeUninit;

pub fn try_build_array<T, E, const N: usize>(
    mut build: impl FnMut(usize) -> Result<T, E>,
) -> Result<[T; N], E> {
    let mut slots: [MaybeUninit<T>; N] =
        std::array::from_fn(|_| MaybeUninit::uninit());

    struct Guard<'a, T> {
        slots: &'a mut [MaybeUninit<T>],
        initialized: usize,
    }

    impl<T> Drop for Guard<'_, T> {
        fn drop(&mut self) {
            for slot in &mut self.slots[..self.initialized] {
                // SAFETY: the guard increments `initialized` only after
                // `write` succeeds, so exactly this prefix contains live T.
                unsafe { slot.assume_init_drop() };
            }
        }
    }

    let mut guard = Guard {
        slots: &mut slots,
        initialized: 0,
    };

    for index in 0..N {
        let value = build(index)?;
        guard.slots[index].write(value);
        guard.initialized += 1;
    }

    std::mem::forget(guard);
    // SAFETY: every slot was initialized exactly once, and the guard no
    // longer drops the elements. The array storage has the same element layout.
    Ok(unsafe { (&slots as *const _ as *const [T; N]).read() })
}
```

The final conversion can be implemented through stable helper patterns appropriate to the pinned toolchain; the central proof remains the initialized prefix and ownership transfer. The source `MaybeUninit` array must not later drop `T` values, which it does not automatically. The guard is forgotten only after full initialization.

If `build` returns an error or panics, the guard drops the live prefix. The uninitialized suffix is ignored. Length is updated after `write`, never before.

### Pointer operation matrix

| Operation | Source requirement | Destination requirement | Overlap | Ownership consequence |
|---|---|---|---|---|
| `ptr::read` | valid initialized `T` | none | n/a | caller now owns copied bits; source must not be used as live `T` unless `Copy` semantics justify it |
| `ptr::write` | value owned by caller | writable aligned storage | n/a | old destination is not dropped |
| `copy_nonoverlapping` | readable initialized range | writable range | forbidden | bitwise duplicate; type ownership must make duplication valid |
| `copy` | readable range | writable range | allowed | same ownership caveat |
| `read_unaligned` | readable initialized bytes for `T` | none | n/a | relaxes alignment only |

A memory operation can satisfy its pointer preconditions and still violate ownership. Copying a `String` bitwise into two live locations creates two owners of one allocation.

### Conservative provenance rules

Until a specific API says otherwise:

- derive interior pointers from the allocation’s original pointer;
- keep the owner live;
- perform arithmetic only within the allocated object and documented one-past range;
- do not fabricate a pointer from an arbitrary integer and dereference it;
- do not merge adjacent allocations into one slice;
- do not create references earlier or longer than necessary;
- preserve raw pointers through documented mapping APIs when changing addresses.

This conservative discipline is more portable than reasoning from numeric addresses. Hardware may treat two integers as ordinary addresses while the language optimizer tracks stronger object identity.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish raw pointers from references and explain why conversion does not transfer ownership, construct one positive and one causal negative example. Mark the first decisive fact in the **initialization and provenance map** and state which evidence could falsify the claim.

2. **Outcome 2.** For use raw borrow operators when creating a reference would itself be invalid, construct one positive and one causal negative example. Mark the first decisive fact in the **initialization and provenance map** and state which evidence could falsify the claim.

3. **Outcome 3.** For derive pointer arithmetic from one allocation and checked element counts, construct one positive and one causal negative example. Mark the first decisive fact in the **initialization and provenance map** and state which evidence could falsify the claim.

4. **Outcome 4.** For use `MaybeUninit` to represent storage that is not yet a valid `T`, construct one positive and one causal negative example. Mark the first decisive fact in the **initialization and provenance map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

FrameVault uses `MaybeUninit` first in an independent batch-construction lab. The capstone’s parser remains safe. The unsafe core gains carefully bounded helpers only where they improve an owning storage abstraction; no raw typed reads are used to decode the archive format.

The matching independent laboratory is [Panic-Safe Batch Builder](../../labs/module-06-panic-safe-batch-builder/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) by recording allocation identity, address, alignment, initialized range, aliasing permission, and lifetime on separate lines. Build the Panic-Safe Batch Builder lab and verify cleanup for every partially initialized state before applying the same reasoning to raw ranges at the FFI boundary.

## Ready to continue

You are ready when you can trace allocation identity, range, alignment, initialization, aliasing, and lifetime independently; build a partially initialized array with correct cleanup; and explain why `NonNull` is not a validity proof.

## Primary Rust references

- [Rust standard library: raw pointers](https://doc.rust-lang.org/std/ptr/index.html)
- [Rust standard library: MaybeUninit](https://doc.rust-lang.org/std/mem/union.MaybeUninit.html)
- [Rust standard library: NonNull](https://doc.rust-lang.org/std/ptr/struct.NonNull.html)
- [Rust Reference: raw borrow operators](https://doc.rust-lang.org/reference/expressions/operator-expr.html#raw-borrow-operators)

## Continue

Continue to [Module 57 — Manual Allocation and Owning Unsafe Abstractions](../module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
