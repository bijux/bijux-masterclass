# Course 6 — Rust Systems Programming

## Bytes, Operating-System Boundaries, Unsafe Abstractions, and FFI

## The promise

Course 6 connects Rust to hostile bytes, filesystems, native paths, child processes, raw storage, allocators, C callers, callbacks, and foreign resources. Unsafe Rust appears only after the safe product contract and proof boundary are explicit.

> **Governing question:** What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations?

Course 5 established disciplined compile-time authority. Course 6 carries the same one-owner rule across external boundaries: bytes, filesystems, native paths, child processes, manual storage, C callers, and foreign resources. Safe APIs remain the product surface; unsafe code is a contained proof obligation, not a design style.

## Before Day 1

You should be able to model ownership and cleanup, design public traits and errors, isolate effects, understand generated code, and maintain deterministic formats and tests.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Define a binary format as a versioned contract rather than a sequence of convenient writes.
- Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.
- Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.
- Construct commands from a program plus arguments, not an interpolated shell line.
- Name the operations Rust requires an unsafe context to perform.
- Distinguish raw pointers from references and explain why conversion does not transfer ownership.
- Construct and validate `Layout` values without unchecked size arithmetic.
- Distinguish ABI compatibility from semantic validity and ownership.
- Separate raw bindings, checked unsafe shims, and safe domain wrappers.
- Draw one boundary map from external bytes to final effects and back to foreign callers.
- Integrate all ten mechanisms in FrameVault without creating competing authorities.
- Complete and defend an unseen change using a whole-system boundary dossier.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing](./module-51-binary-data-contracts/index.md) | How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning? | **Define a binary format as a versioned contract rather than a sequence of convenient writes.** | [Checked Frame Codec](../labs/module-01-checked-frame-codec/README.md) |
| 2 | [52 — Files, Durability, and Transactional Replacement](./module-52-files-durability-and-transactional-replacement/index.md) | What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state? | **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.** | [Atomic Archive Store](../labs/module-02-atomic-archive-store/README.md) |
| 3 | [53 — Paths, Names, and Platform Boundaries](./module-53-paths-names-and-platform-boundaries/index.md) | How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable? | **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.** | [Sandboxed Extraction Paths](../labs/module-03-sandboxed-extraction-paths/README.md) |
| 4 | [54 — Processes, Environments, and Standard Streams](./module-54-processes-environments-and-standard-streams/index.md) | How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result? | **Construct commands from a program plus arguments, not an interpolated shell line.** | [Bounded Process Capture](../labs/module-04-bounded-process-capture/README.md) |
| 5 | [55 — Unsafe Rust as a Proof Boundary](./module-55-unsafe-rust-and-safety-proofs/index.md) | What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable? | **Name the operations Rust requires an unsafe context to perform.** | [Unsafe Slice Kernel](../labs/module-05-unsafe-slice-kernel/README.md) |
| 6 | [56 — Raw Pointers, Provenance, and Uninitialized Memory](./module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) | How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation? | **Distinguish raw pointers from references and explain why conversion does not transfer ownership.** | [Panic-Safe Batch Builder](../labs/module-06-panic-safe-batch-builder/README.md) |
| 7 | [57 — Manual Allocation and Owning Unsafe Abstractions](./module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) | How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state? | **Construct and validate `Layout` values without unchecked size arithmetic.** | [Aligned Byte Buffer](../labs/module-07-aligned-byte-buffer/README.md) |
| 8 | [58 — C FFI: ABI, Strings, Pointers, and Error Boundaries](./module-58-c-ffi-abi-strings-and-error-boundaries/index.md) | How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides? | **Distinguish ABI compatibility from semantic validity and ownership.** | [C ABI Line Validator](../labs/module-08-c-abi-archive-validator/README.md) |
| 9 | [59 — Foreign Resources, Callbacks, and Wrapper Architecture](./module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) | How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations? | **Separate raw bindings, checked unsafe shims, and safe domain wrappers.** | [Opaque Foreign Session](../labs/module-09-opaque-foreign-session/README.md) |
| 10 | [60 — Integrated Systems Design, Testing, and Audit](./module-60-integrated-systems-design-and-audit/index.md) | How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another? | **Draw one boundary map from external bytes to final effects and back to foreign callers.** | [Systems Boundary Audit](../labs/module-10-systems-boundary-audit/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Bytes | Check ranges and arithmetic before conversion or allocation. |
| File commit | Separate candidate construction, visibility, replacement, and durability. |
| Unsafe | Write the safety preconditions before the unsafe operation and expose a safe interface that enforces them. |
| Allocation | Store the exact layout and initialized-state facts needed for cleanup. |
| FFI | Specify representation, nullability, ownership, failure, panic, callback retention, and thread rules on both sides. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **whole-system boundary dossier**. Write the external representation, validity checks, resource states, unsafe obligations, cleanup, and platform assumptions before crossing the boundary. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible.

Course 7 introduces legal schedules: values and resources now move among threads, synchronization carries visibility, and termination becomes a first-class product property.

## Capstone — FrameVault

FrameVault is a versioned binary archive with checked parsing, transactional replacement, extraction policy, process capture, one manual allocation owner, and a C ABI with opaque sessions and callback rules.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a checked packet archive with transactional output, one justified unsafe storage abstraction or a written rejection of it, and a stateless C validation boundary.

and then change the capstone under this constraint:

> Add a bounded archive index to FrameVault while preserving format compatibility, path policy, failure atomicity, allocator safety, and C ABI ownership.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing](./module-51-binary-data-contracts/index.md)
- [FrameVault engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
