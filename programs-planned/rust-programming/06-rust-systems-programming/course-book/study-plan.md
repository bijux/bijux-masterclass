# Course 6 study plan — Rust Systems Programming

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and FrameVault increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | FrameVault increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing

**Governing question:** How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?

### Morning: derive the model

Read [Module 51](module-51-binary-data-contracts/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-51-binary-data-contracts/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 51 — Checked Frame Codec](../labs/module-01-checked-frame-codec/README.md). Build a small versioned binary frame format. Each frame contains a kind byte, a little-endian payload length, the payload, and an integrity checksum. The decoder must treat every byte as untrusted and report the exact offset of failure.

### Evening: integrate the course product

FrameVault begins with a format module containing the magic bytes, limits, checked cursor, encoder, decoder, checksum, and typed errors. The first increment must round-trip empty archives, text and binary payloads, reject truncation at every byte boundary, reject oversized declarations before allocation, reject unknown flags, and reject trailing bytes.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 2 — Files, Durability, and Transactional Replacement

**Governing question:** What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

### Morning: derive the model

Read [Module 52](module-52-files-durability-and-transactional-replacement/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-52-files-durability-and-transactional-replacement/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 52 — Atomic Archive Store](../labs/module-02-atomic-archive-store/README.md). Build a file replacement component that preserves the previous valid destination until a complete staged file has been written, flushed, synchronized, and renamed.

### Evening: integrate the course product

FrameVault adds `store.rs`: bounded file loading, complete encoding before commit, same-directory temporary creation with `create_new`, `write_all`, `flush`, `sync_all`, and replacement. Its documentation promises failure-atomic replacement with respect to pre-rename errors on supported local usage, not universal crash durability. Tests retain the previous archive when encoding or temporary writing fails.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 3 — Paths, Names, and Platform Boundaries

**Governing question:** How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

### Morning: derive the model

Read [Module 53](module-53-paths-names-and-platform-boundaries/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-53-paths-names-and-platform-boundaries/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 53 — Sandboxed Extraction Paths](../labs/module-03-sandboxed-extraction-paths/README.md). Build a portable logical-path parser and a bounded extraction resolver. The lab separates archive syntax from host path syntax and refuses direct parent, root, prefix, empty, and dot components.

### Evening: integrate the course product

FrameVault adds a `LogicalPath` type for archive names and a path-policy module for packing and extraction. Extraction rejects absolute forms, empty components, `.` and `..`, NUL, excessive length, and any existing symlink component in its controlled destination tree. Host-path conversion rejects non-UTF-8 components with a typed error; diagnostics preserve the original `PathBuf`.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 4 — Processes, Environments, and Standard Streams

**Governing question:** How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

### Morning: derive the model

Read [Module 54](module-54-processes-environments-and-standard-streams/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-54-processes-environments-and-standard-streams/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 54 — Bounded Process Capture](../labs/module-04-bounded-process-capture/README.md). Build a structured process request and finite-output capture adapter. Program, arguments, working directory, and environment changes remain separate OS strings. Output remains bytes and nonzero status remains structured.

### Evening: integrate the course product

FrameVault adds a command-capture record. `capture` invokes a program directly through `Command`, closes stdin, captures bounded stdout and stderr, records the supplied program and arguments as UTF-8 only when representable, and stores a portable exit-status model. It rejects captures whose combined output exceeds the configured limit and documents that untrusted long-running commands require later containment work.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 5 — Unsafe Rust as a Proof Boundary

**Governing question:** What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

### Morning: derive the model

Read [Module 55](module-55-unsafe-rust-and-safety-proofs/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-55-unsafe-rust-and-safety-proofs/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 55 — Unsafe Slice Kernel](../labs/module-05-unsafe-slice-kernel/README.md). Build a safe API that returns two distinct mutable elements from one slice. First implement a safe reference version with `split_at_mut`, then implement a narrow raw-pointer kernel and prove that both expose the same behavior.

### Evening: integrate the course product

FrameVault creates an `unsafe_core` boundary. Before implementation, it contains a safety dossier: every unsafe operation, its preconditions, the type invariant that proves them, panic behavior, zero-length behavior, and destruction path. The first kernel is a checked two-index mutable borrow used only as a focused exercise; the capstone later adds an owned aligned byte allocation.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 6 — Raw Pointers, Provenance, and Uninitialized Memory

**Governing question:** How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

### Morning: derive the model

Read [Module 56](module-56-raw-pointers-provenance-and-uninitialized-memory/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-56-raw-pointers-provenance-and-uninitialized-memory/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 56 — Panic-Safe Batch Builder](../labs/module-06-panic-safe-batch-builder/README.md). Build a fixed-size array through `MaybeUninit` while an element constructor can return an error or panic. The product must drop exactly the initialized prefix and never treat the suffix as live values.

### Evening: integrate the course product

FrameVault uses `MaybeUninit` first in an independent batch-construction lab. The capstone’s parser remains safe. The unsafe core gains carefully bounded helpers only where they improve an owning storage abstraction; no raw typed reads are used to decode the archive format.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 7 — Manual Allocation and Owning Unsafe Abstractions

**Governing question:** How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?

### Morning: derive the model

Read [Module 57](module-57-manual-allocation-and-owning-unsafe-abstractions/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-57-manual-allocation-and-owning-unsafe-abstractions/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 57 — Aligned Byte Buffer](../labs/module-07-aligned-byte-buffer/README.md). Build a fixed-length, zero-initialized byte owner using the global allocator. The public API is safe; the implementation owns one exact allocation layout and exposes only slices tied to ordinary borrows.

### Evening: integrate the course product

FrameVault adds `AlignedBytes`, a fixed-length zero-initialized byte owner with validated power-of-two alignment, explicit zero-length state, borrowed slice access, and exact deallocation. The file loader may choose it for staging an archive of known bounded size. The parser still receives an ordinary `&[u8]`, so unsafe storage does not leak into format logic.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 8 — C FFI: ABI, Strings, Pointers, and Error Boundaries

**Governing question:** How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

### Morning: derive the model

Read [Module 58](module-58-c-ffi-abi-strings-and-error-boundaries/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-58-c-ffi-abi-strings-and-error-boundaries/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 58 — C ABI Line Validator](../labs/module-08-c-abi-archive-validator/README.md). Expose a small C-compatible function that validates a byte buffer as newline-delimited UTF-8 records and fills a `repr(C)` report. The lab focuses on pointer-plus-length, out-parameter initialization, stable status codes, and panic containment.

### Evening: integrate the course product

FrameVault exports a stateless `framevault_validate` C function over pointer-plus-length bytes and a `repr(C)` report. It checks null cases it can observe, converts the input to a slice under a documented safety contract, catches unwinding panics where the build strategy permits, maps errors to stable codes, and never returns Rust-owned borrowed text.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 9 — Foreign Resources, Callbacks, and Wrapper Architecture

**Governing question:** How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?

### Morning: derive the model

Read [Module 59](module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-59-foreign-resources-callbacks-and-wrapper-architecture/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 59 — Opaque Foreign Session](../labs/module-09-opaque-foreign-session/README.md). Expose an opaque Rust-owned counter session through a C ABI. The interface creates one ownership obligation, supports synchronous callback enumeration, and consumes the session exactly once through a matching free function.

### Evening: integrate the course product

FrameVault adds an opaque `FvSession` C API. `framevault_open` validates and owns decoded archive data; `framevault_entry_count` reads metadata; `framevault_for_each_entry` invokes a synchronous callback with temporary name bytes; `framevault_free` consumes the handle. Rust-side tests exercise open, enumerate, early stop, and free through the exported functions without requiring a C compiler.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract
## Day 10 — Integrated Systems Design, Testing, and Audit

**Governing question:** How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

### Morning: derive the model

Read [Module 60](module-60-integrated-systems-design-and-audit/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-60-integrated-systems-design-and-audit/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 60 — Systems Boundary Audit](../labs/module-10-systems-boundary-audit/README.md). Build a compact packet inspector that integrates a checked binary format, transactional file output, and a stateless C validator. Then produce a boundary map and safety dossier that another engineer can review without reading implementation folklore.

### Evening: integrate the course product

FrameVault is completed as a library, CLI, and C-compatible library. The final increment adds golden-format fixtures, exhaustive truncation tests, path-adversary tests, deterministic self-child process capture, aligned-buffer tests, ABI session tests, a safety dossier, a compatibility table, and a demonstration script. The CLI supports create, list, verify, extract, capture, help, and version.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- reconstruct the module invariant without the chapter
- complete the lab and transfer without weakening the contract


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend FrameVault by tracing one successful operation and one adversarial failure through every layer touched by the course.
