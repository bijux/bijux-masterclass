# Course 6 — Rust Systems Programming

## Bytes, Operating-System Boundaries, Unsafe Abstractions, and FFI

Cross external boundaries without losing the guarantees built in the first five courses: define representations, track resources, isolate unsafe obligations, and expose safe interfaces with claims no stronger than the platform evidence.

## Why this course exists

Earlier courses mostly begin after a valid Rust value exists. Systems work begins before that point and continues after Rust has delegated work to a filesystem, process, allocator, or foreign caller. Every boundary introduces facts the compiler cannot establish alone: byte order, path interpretation, short I/O, durability, pointer validity, allocation layout, ABI agreement, callback lifetime, and external behavior. This course turns those facts into explicit representations, state machines, safety contracts, and narrow safe interfaces.

## Before you begin

Courses 1–5, including exact ownership and lifetime reasoning, RAII, representation claims, trait-based architecture, explicit effect boundaries, deterministic generation, and causal testing.

Keep a representation table, resource-state machine, boundary ledger, unsafe safety ledger, and ABI contract beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Define a versioned binary format before implementation, including widths, endianness, limits, canonical encoding, unknown-value policy, and trailing-data policy.
- Decode hostile bytes with checked ranges and checked arithmetic before allocation, reference creation, UTF-8 construction, or cursor advancement.
- Distinguish corruption detection from authentication and structural decoding from domain validation.
- Handle short reads and writes and distinguish write completion, flush, file synchronization, rename visibility, directory synchronization, and honest durability claims.
- Design failure-atomic same-directory replacement with explicit pre-commit and post-commit failure states and cleanup ownership.
- Keep portable logical names distinct from native `Path`/`OsStr` values, reject traversal by components, and state the limits of pathname preflight under races.
- Launch child programs from an executable plus argument vector, control environment and working-directory policy, preserve byte streams and status, and avoid shell interpolation.
- Define an unsafe boundary by exact operations, preconditions, establishing code, validity duration, panic behavior, cleanup, and safe-caller protection.
- Manipulate raw pointers and `MaybeUninit` while tracking allocation origin, range, alignment, initialization, aliasing, provenance, and lifetime separately.
- Build panic-safe partial initialization with a guard that destroys exactly the initialized prefix and never treats uninitialized storage as a live value.
- Construct one owning manual-allocation abstraction whose empty state, layout, slice exposure, movement, failure, and deallocation are correct.
- Match Rust and C declarations across ABI, widths, representation, nullability, strings, output initialization, status codes, and panic containment.
- Wrap opaque foreign resources with exactly-once ownership transfer, synchronous borrowing, callback lifetime rules, reentrancy limits, and explicit release.
- Classify each success claim as language guarantee, library contract, target-conditioned behavior, operating-system result, foreign obligation, or unclaimed property.
- Audit an integrated systems product across representation, bounds, filesystem state, paths, process lifecycle, unsafe invariants, allocation, ABI, compatibility, and adversarial tests.

## What this course deliberately leaves for later

The course is single-threaded and synchronous. Atomics, shared-memory concurrency, parallel work scheduling, asynchronous I/O, networking, and production profiling are reserved for Courses 7–9.

## Ten-day route

1. [Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing](module-51-binary-data-contracts/index.md) — How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?
2. [Module 52: Files, Durability, and Transactional Replacement](module-52-files-durability-and-transactional-replacement/index.md) — What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?
3. [Module 53: Paths, Names, and Platform Boundaries](module-53-paths-names-and-platform-boundaries/index.md) — How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?
4. [Module 54: Processes, Environments, and Standard Streams](module-54-processes-environments-and-standard-streams/index.md) — How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?
5. [Module 55: Unsafe Rust as a Proof Boundary](module-55-unsafe-rust-and-safety-proofs/index.md) — What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?
6. [Module 56: Raw Pointers, Provenance, and Uninitialized Memory](module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) — How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?
7. [Module 57: Manual Allocation and Owning Unsafe Abstractions](module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) — How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?
8. [Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries](module-58-c-ffi-abi-strings-and-error-boundaries/index.md) — How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?
9. [Module 59: Foreign Resources, Callbacks, and Wrapper Architecture](module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) — How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?
10. [Module 60: Integrated Systems Design, Testing, and Audit](module-60-integrated-systems-design-and-audit/index.md) — How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **FrameVault**: a versioned archive, transactional store, path policy, child-process capture system, aligned storage owner, C ABI, and opaque foreign-session API with an explicit safety and compatibility dossier. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [FrameVault engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 7 will add concurrency and parallelism, where every ownership, cleanup, unsafe, and external-boundary claim must remain valid under simultaneous execution.

[Return to the program start](../../README.md) · [Open the sixty-module map](../../COURSE_MAP.md)
