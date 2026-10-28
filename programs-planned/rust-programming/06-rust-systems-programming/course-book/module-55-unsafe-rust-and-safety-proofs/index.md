# 55 — Unsafe Rust as a Proof Boundary

**Course 6, day 5 · Module 55 of 60**  
`██████████████████░░` **55/60**

[← Module 54: Processes, Environments, and Standard Streams](../module-54-processes-environments-and-standard-streams/index.md) · [Course 6 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 56: Raw Pointers, Provenance, and Uninitialized Memory →](../module-56-raw-pointers-provenance-and-uninitialized-memory/index.md)

## The question

> What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

## Why this comes now

The first four modules deliberately solved systems problems with safe Rust. That ordering matters. `unsafe` is not a badge of low-level seriousness and it does not make code faster by itself. It is a mechanism for expressing a proof the compiler cannot complete. Module 55 introduces the proof discipline before raw pointers and allocators create more ways to be wrong.

## What you will be able to do

- Name the operations Rust requires an unsafe context to perform.
- Distinguish compiler permission from semantic safety and undefined behavior.
- Write safety preconditions, internal invariants, and postconditions before an unsafe block.
- Keep unsafe operations inside narrow private modules with safe public APIs.
- Use `unsafe fn`, unsafe traits, and unsafe attributes only when their contracts require caller or implementor proof.
- Review unsafe code through explicit claims rather than intuition or successful tests.

## Core model

### Unsafe Rust obeys the same language rules

Unsafe Rust does not switch to a different language where anything is permitted. The Rust Reference still defines valid values, aliasing obligations, alignment, initialization, lifetimes, and undefined behavior. An `unsafe` block only permits a small set of operations whose preconditions the compiler cannot verify.

Current Rust permits unsafe code to dereference raw pointers, call unsafe functions, access mutable statics, access union fields, and implement unsafe traits. Some attributes, including exported symbol controls such as `no_mangle`, are themselves unsafe in Rust 2024 because they impose global obligations.

If an unsafe operation violates its contract, the program can have undefined behavior even if the immediate output looks correct. Tests are evidence over executions; they are not a proof that every optimizer assumption remains valid.

### Unsafe is an obligation ledger

Before each unsafe block, write the facts that make the operation valid:

```rust
// SAFETY:
// - `pointer` was allocated for `length` initialized bytes.
// - the allocation remains alive for the returned slice lifetime.
// - no mutable access exists while the shared slice is used.
// - `pointer` is non-null and aligned for `u8`.
unsafe { std::slice::from_raw_parts(pointer, length) }
```

A useful ledger has four parts:

1. **Required preconditions** — facts demanded by the unsafe operation.
2. **Evidence** — checks, type invariants, ownership, or platform contracts that establish them.
3. **Preserved invariants** — facts that must remain true while the result is used.
4. **Postconditions** — what safe callers may rely on afterward.

“Pointer came from C” or “length was checked” is not enough. State checked against what, who owns the allocation, how long it lives, and what aliasing is allowed.

### Undefined behavior is broader than a crash

Undefined behavior includes invalid pointer dereference, out-of-bounds pointer arithmetic, data races, invalid value production, misaligned references, violation of aliasing assumptions, and unwinding across an ABI boundary that forbids it. It may appear as a crash, silent corruption, impossible branch elimination, or different behavior after a harmless refactor.

The Reference’s list is authoritative but not necessarily exhaustive as the memory model evolves. Conservative systems code avoids relying on unclear provenance or aliasing tricks. “It works on my machine” is especially weak evidence where optimizations are involved.

### Make the unsafe region smaller than the abstraction

A safe abstraction can contain unsafe implementation details. The unsafe block should wrap only the operation requiring proof, not the entire function:

```rust
pub fn get_pair_mut<T>(slice: &mut [T], a: usize, b: usize)
    -> Option<(&mut T, &mut T)>
{
    if a == b || a >= slice.len() || b >= slice.len() {
        return None;
    }
    let pointer = slice.as_mut_ptr();
    // SAFETY: bounds and distinctness were checked; the input borrow owns
    // exclusive access to the whole slice for the returned lifetime.
    unsafe { Some((&mut *pointer.add(a), &mut *pointer.add(b))) }
}
```

All validation remains in safe code. The unsafe block is one expression whose proof can be reviewed directly.

### Privacy reduces the trusted surface

Unsafe code must be able to rely on invariants that safe callers cannot violate. Private fields and constructors enforce those invariants. If a safe caller can create an invalid internal state, later unsafe code cannot assume the invariant.

A good module structure is:

```text
public safe API
    ↓ validates and owns state
private invariant-bearing type
    ↓ calls
small unsafe kernel
```

Do not expose raw fields merely for convenience. If a raw escape hatch is necessary, mark it unsafe and document exactly what the caller must prove.

### `unsafe fn` assigns obligations to the caller

An unsafe function should be unsafe because calling it correctly requires facts the type system cannot express or the function cannot check. Its documentation needs a `# Safety` section.

Inside an unsafe function, unsafe operations should still appear in explicit unsafe blocks. Rust 2024’s `unsafe_op_in_unsafe_fn` discipline makes this boundary visible: the function signature states the caller’s obligation, while each block states how the implementation discharges local obligations.

Do not mark a function unsafe only because its implementation uses unsafe operations. If the function can validate everything and present a safe contract, keep the public function safe.

### Unsafe traits are promises to other unsafe code

An unsafe trait means incorrect implementation can allow other code to cause undefined behavior. `Send` and `Sync` are canonical examples: unsafe code may rely on their truth when moving or sharing values across threads.

The trait documentation must state implementation requirements. An unsafe implementation should include a safety argument tied to the concrete fields and invariants. Empty marker traits can carry enormous obligations even though they contain no methods.

Course 6 avoids custom concurrency traits, which belong to Course 7, but the principle applies to foreign-resource markers and trusted byte-representation traits as well.

### Unsafe attributes affect global program contracts

Rust 2024 writes certain attributes as `#[unsafe(...)]`, for example:

```rust
#[unsafe(no_mangle)]
pub extern "C" fn framevault_version() -> u32 { 1 }
```

The obligation is global: the chosen symbol name must not collide incompatibly, the ABI and signature must match external expectations, and the exported function must uphold its boundary contract. The body can be entirely safe while the attribute remains unsafe.

This is a useful reminder that unsafety is not synonymous with raw pointer syntax. It marks a proof obligation the compiler cannot verify.

### Panic safety is part of memory safety in unsafe code

An unsafe abstraction must remain memory-safe if safe code it invokes panics. Examples include cloning elements during buffer growth or invoking a callback while partially initialized state exists.

Use state that always describes the initialized prefix. Update length only after initialization succeeds. Place cleanup responsibility in RAII guards. Never temporarily create two owners and hope the operation between them cannot panic.

Course 2 introduced unwind-aware RAII. Course 6 now treats it as a required part of every owning unsafe abstraction.

### Audit the abstraction, not only the block

A complete review follows data from safe input through invariant construction, unsafe operation, returned value, mutation methods, `Drop`, and trait implementations. Questions include:

- Can safe code create an invalid state?
- Are pointer and length derived from the same allocation?
- Can reallocation invalidate a reference?
- Can panic expose a false length?
- Are zero-sized and zero-length cases handled?
- Are `Send` and `Sync` inherited or implemented correctly?
- Can `Drop` run twice or on partially initialized memory?
- Does FFI permit a callback to retain a temporary pointer?

The proof boundary is the whole abstraction contract, even when the syntactic unsafe block is one line.

### Use tools as evidence, not as the contract

Miri can detect many forms of undefined behavior in executed paths. Sanitizers can find memory and race errors on supported targets. Fuzzing can explore parser and FFI inputs. Clippy can require documented unsafe blocks. None replaces the written invariant.

The strongest workflow combines static review, executable tests, dynamic tools, and a deliberately small unsafe surface. A tool’s silence means only that the tested execution did not trigger a detected violation.

### A safety-review worksheet

For every unsafe operation, fill this table before implementation:

| Field | Question |
|---|---|
| operation | Which exact library or language operation requires unsafe? |
| preconditions | What must be true about pointer, range, value, aliasing, lifetime, ABI, or global symbol? |
| evidence source | Which check, private field invariant, owner, or external contract establishes each fact? |
| invalidation | Which later mutation, panic, callback, reallocation, or destructor could make the fact false? |
| result lifetime | To which real owner borrow is any returned reference tied? |
| cleanup | Who drops values and deallocates storage on every path? |
| tool evidence | Which Miri, sanitizer, fuzz, compile-fail, or integration test exercises the claim? |

A safety comment is the compressed result of this worksheet, not a slogan added after code review.

### Unsafe API classification

Consider three functions:

```rust
pub fn pair_mut<T>(slice: &mut [T], a: usize, b: usize)
    -> Option<(&mut T, &mut T)>;

pub unsafe fn pair_mut_unchecked<T>(
    slice: &mut [T],
    a: usize,
    b: usize,
) -> (&mut T, &mut T);

fn pair_mut_kernel<T>(
    pointer: *mut T,
    a: usize,
    b: usize,
) -> (*mut T, *mut T);
```

The safe function validates bounds and distinctness. The unchecked function assigns those obligations to the caller and needs a `# Safety` section. The private kernel may not need to be `unsafe fn` if it only computes raw pointers without dereferencing; the actual dereference remains in an unsafe block where the evidence is visible. API unsafety follows caller obligations, not a desire to label low-level code.

### The unsafe dependency cone

An unsafe block relies on more than the lines above it. If it trusts `self.length <= self.capacity`, every safe method that mutates either field belongs to the trusted cone. If it trusts that a callback is synchronous, the foreign-library version and configuration belong to the cone. If it trusts a generated C header, the build and release process belong to the cone.

A review should therefore list:

```text
unsafe operation
    ← local checks
    ← constructor invariants
    ← all safe mutators
    ← drop behavior
    ← trait implementations
    ← foreign/platform contracts
```

Privacy narrows this cone. Public fields and broad unsafe helpers enlarge it.

### Logic errors versus undefined behavior

A safe archive parser that returns the wrong entry name has a logic error. It may cause data loss, but safe Rust still constrains memory behavior. An unsafe parser that creates a reference to uninitialized bytes can have undefined behavior. The product must prevent both, but the review urgency differs: memory-safety invariants cannot be delegated to callers of a safe API.

Do not use “safe” to mean correct, secure, or panic-free. It means the language’s memory and type safety obligations are upheld. Course 6 maintains separate ledgers for memory safety, product correctness, and threat policy.

## Use the idea in a complete program

FrameVault creates an `unsafe_core` boundary. Before implementation, it contains a safety dossier: every unsafe operation, its preconditions, the type invariant that proves them, panic behavior, zero-length behavior, and destruction path. The first kernel is a checked two-index mutable borrow used only as a focused exercise; the capstone later adds an owned aligned byte allocation.

The matching independent laboratory is [Unsafe Slice Kernel](../../labs/module-05-unsafe-slice-kernel/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) with a safety ledger for every unchecked operation. Build the Unsafe Slice Kernel lab, reduce the public preconditions as far as the design allows, and then review each FrameVault unsafe block from its reachable safe caller rather than from the block in isolation.

## Ready to continue

You are ready when you can write a line-by-line safety argument, decide whether the caller or implementation owns each proof, and reject an unsafe abstraction whose private invariant, panic path, or destructor has not been analyzed.

## Primary Rust references

- [Rust Reference: unsafe keyword](https://doc.rust-lang.org/reference/unsafe-keyword.html)
- [Rust Reference: undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)
- [Rustonomicon: working with unsafe](https://doc.rust-lang.org/nomicon/working-with-unsafe.html)
- [Rust Reference: unsafe attributes](https://doc.rust-lang.org/reference/attributes.html#attributes-safety)

## Continue

1. Complete the [Module 55 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 55 — Unsafe Slice Kernel](../../labs/module-05-unsafe-slice-kernel/README.md) from its public contract.
3. Apply the Module 55 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
