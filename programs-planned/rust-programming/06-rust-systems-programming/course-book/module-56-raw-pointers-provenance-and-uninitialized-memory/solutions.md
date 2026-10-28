# Reasoned solutions — Module 56: Raw Pointers, Provenance, and Uninitialized Memory

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the FrameVault engineering guide](../capstone.md)

Use these solutions after freezing your own analysis. The code result matters less than locating the first broken contract and identifying who owns the repair.

Read each answer as a boundary proof: identify the missing fact, the component able to establish it, and the state that must remain unchanged when the proof fails.

## Prediction analysis

### Prediction 1

**Problem.** A raw pointer is copied after its allocation is freed. Is copying itself the dereference error?

**Reasoned answer.** Copying the address is generally permitted; using it as if live is the problem.

### Prediction 2

**Problem.** `&packed.field as *const _` is used on an unaligned field. What can already be wrong?

**Reasoned answer.** The intermediate reference must be aligned, so creating it can be undefined behavior.

### Prediction 3

**Problem.** A byte pointer is cast to `*const u32`. Which obligations remain?

**Reasoned answer.** Bounds, alignment, initialization, provenance, representation, and aliasing all remain.

### Prediction 4

**Problem.** `ptr::read` extracts a `String`, then the original location is dropped normally. What happens?

**Reasoned answer.** The same ownership can be dropped twice.

### Prediction 5

**Problem.** `ptr::write` overwrites an initialized `String`. What happens to the old value?

**Reasoned answer.** It is not dropped and is leaked unless moved or dropped first.

### Prediction 6

**Problem.** `MaybeUninit<bool>` is uninitialized. May it be read as `bool`?

**Reasoned answer.** No. Only initialized valid bit patterns may become a live `bool`.

### Prediction 7

**Problem.** `NonNull<T>` is present. Does it prove one live `T` exists?

**Reasoned answer.** No. It proves only non-nullness at the type level.

### Prediction 8

**Problem.** A raw slice length crosses two adjacent allocations. Is the numeric range enough?

**Reasoned answer.** No. The slice range must belong to one allocation under the API contract.

## Construction guidance

### Batch guard

The guard owns the slots and count until success. On failure it drops exactly the initialized prefix; on success its cleanup is disabled after ownership transfer.

### Array conversion

All slots must be initialized, the layout must match, and the source wrapper must not later drop the same elements.

### Header operation

Endian-aware byte conversion is alignment-independent and expresses the file contract; raw loads add obligations without benefit here.

### Pointer round trip

Numeric equality is not a complete portable pointer proof. Keep the original pointer and use documented address-manipulation APIs only when required.

### FFI transfer

The foreign contract must report an initialized count no greater than capacity, and Rust must drop only that prefix on every return path.

## Boundary-trace reference

A strong solution trace for this module must for every raw pointer, record allocation origin, provenance, numeric range, alignment, initialized subrange, active aliasing permission, lifetime owner, and destruction responsibility. For partially initialized storage, show the prefix length after each successful element construction. It should reveal the earliest point at which an invalid assumption would become observable and the unique owner responsible for cleanup or rollback.

## Weak repairs to reject

Reject solutions built around these shortcuts:

- forming a reference before pointer validity is established;
- treating a non-null address as proof of liveness;
- using pointer arithmetic outside the originating allocation;
- assuming zeroed bytes form an arbitrary valid `T`;
- calling `assume_init` before every field or element is initialized;
- forgetting cleanup for a panic during element construction;

A principled repair makes the missing fact explicit in a type, checked operation, state transition, safety contract, platform qualification, or foreign-call contract. It does not merely move the assumption to a less visible line.

## Raw-storage state model

Treat allocation, initialization, and references as distinct axes:

```text
unallocated
  -> allocated / zero initialized elements
  -> allocated / initialized prefix 0..k
  -> allocated / fully initialized
  -> borrowed through valid references
  -> elements dropped
  -> allocation deallocated
```

A pointer value alone does not identify which state holds. `MaybeUninit<T>` prevents Rust from assuming a `T` exists, but it does not track the initialized prefix for you. The guard or builder must do that explicitly.

| Operation | Proof obligation |
|---|---|
| `ptr.add(i)` | resulting pointer remains within or one-past the same allocation and arithmetic does not overflow |
| `ptr.write(value)` | destination is suitably aligned, valid for writes, and not currently initialized in a way that would leak a required destructor |
| `assume_init_ref` | the exact element is fully initialized and remains live for the reference |
| `drop_in_place` | a valid initialized value exists and has not already been dropped |
| `from_raw_parts` | range, alignment, provenance, lifetime, and aliasing all hold together |

## Panic-safety clinic

A batch builder that initializes elements in a loop must update its initialized count only after each successful write. During unwinding, the guard drops exactly `0..initialized` and then releases the allocation. Updating the count before the write risks dropping uninitialized memory; updating it too late can leak the newly written value if later code panics.

Do not create a reference merely to inspect whether memory is valid. Reference creation itself asserts validity and aliasing obligations. Keep uncertain storage in pointer or `MaybeUninit` form until every fact required by the reference is established.

## Completion check

Use the chapter’s readiness statement as the first threshold:

You are ready when you can trace allocation identity, range, alignment, initialization, aliasing, and lifetime independently; build a partially initialized array with correct cleanup; and explain why `NonNull` is not a validity proof.

Then perform this destructive regression check: force construction to panic at every prefix length and verify that each initialized element is dropped exactly once while uninitialized slots are never dropped. The resulting failure should be caught for the causal reason predicted in the workbook, not by an unrelated panic or syntax error.
