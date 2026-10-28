# Course 6 — Rust Systems Programming

## Bytes, Operating-System Boundaries, Unsafe Abstractions, and FFI

Course 6 connects Rust to hostile bytes, filesystems, native paths, child processes, raw storage, allocators, C callers, callbacks, and foreign resources. Unsafe Rust appears only after the safe product contract and proof boundary are explicit.

> **Governing question:** What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations?

## Entry point

You should be able to model ownership and cleanup, design public traits and errors, isolate effects, understand generated code, and maintain deterministic formats and tests.

The immediate prerequisite is [Course 5: Rust Metaprogramming](../05-rust-metaprogramming/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing](course-book/module-51-binary-data-contracts/index.md) | Define a binary format as a versioned contract rather than a sequence of convenient writes | [Checked Frame Codec](labs/module-01-checked-frame-codec/README.md) |
| 2 | [52 — Files, Durability, and Transactional Replacement](course-book/module-52-files-durability-and-transactional-replacement/index.md) | Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability | [Atomic Archive Store](labs/module-02-atomic-archive-store/README.md) |
| 3 | [53 — Paths, Names, and Platform Boundaries](course-book/module-53-paths-names-and-platform-boundaries/index.md) | Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text | [Sandboxed Extraction Paths](labs/module-03-sandboxed-extraction-paths/README.md) |
| 4 | [54 — Processes, Environments, and Standard Streams](course-book/module-54-processes-environments-and-standard-streams/index.md) | Construct commands from a program plus arguments, not an interpolated shell line | [Bounded Process Capture](labs/module-04-bounded-process-capture/README.md) |
| 5 | [55 — Unsafe Rust as a Proof Boundary](course-book/module-55-unsafe-rust-and-safety-proofs/index.md) | Name the operations Rust requires an unsafe context to perform | [Unsafe Slice Kernel](labs/module-05-unsafe-slice-kernel/README.md) |
| 6 | [56 — Raw Pointers, Provenance, and Uninitialized Memory](course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) | Distinguish raw pointers from references and explain why conversion does not transfer ownership | [Panic-Safe Batch Builder](labs/module-06-panic-safe-batch-builder/README.md) |
| 7 | [57 — Manual Allocation and Owning Unsafe Abstractions](course-book/module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) | Construct and validate `Layout` values without unchecked size arithmetic | [Aligned Byte Buffer](labs/module-07-aligned-byte-buffer/README.md) |
| 8 | [58 — C FFI: ABI, Strings, Pointers, and Error Boundaries](course-book/module-58-c-ffi-abi-strings-and-error-boundaries/index.md) | Distinguish ABI compatibility from semantic validity and ownership | [C ABI Line Validator](labs/module-08-c-abi-archive-validator/README.md) |
| 9 | [59 — Foreign Resources, Callbacks, and Wrapper Architecture](course-book/module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) | Separate raw bindings, checked unsafe shims, and safe domain wrappers | [Opaque Foreign Session](labs/module-09-opaque-foreign-session/README.md) |
| 10 | [60 — Integrated Systems Design, Testing, and Audit](course-book/module-60-integrated-systems-design-and-audit/index.md) | Draw one boundary map from external bytes to final effects and back to foreign callers | [Systems Boundary Audit](labs/module-10-systems-boundary-audit/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Write the external representation, validity checks, resource states, unsafe obligations, cleanup, and platform assumptions before crossing the boundary. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — FrameVault

FrameVault is a versioned binary archive with checked parsing, transactional replacement, extraction policy, process capture, one manual allocation owner, and a C ABI with opaque sessions and callback rules.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible.

Course 7 introduces legal schedules: values and resources now move among threads, synchronization carries visibility, and termination becomes a first-class product property.

## Exit standard

Complete this independent construction:

> Build a checked packet archive with transactional output, one justified unsafe storage abstraction or a written rejection of it, and a stateless C validation boundary.

Then complete this capstone extension:

> Add a bounded archive index to FrameVault while preserving format compatibility, path policy, failure atomicity, allocator safety, and C ABI ownership.

The next step is [Course 7: Rust Concurrency and Parallelism](../07-rust-concurrency-parallelism/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
