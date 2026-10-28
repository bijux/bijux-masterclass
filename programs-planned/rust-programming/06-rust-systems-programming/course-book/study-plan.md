# Course 6 Study Plan — Rust Systems Programming

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations?** answerable through construction and explanation.

## Daily rhythm

Use a **whole-system boundary dossier** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 51: Binary Data Contracts: Bytes, Endianness, and Checked Parsing

**Question:** How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?

**Retrieval:** Without notes, restate the invariant carried from Module 50 — Build Scripts, Generated Code, and Compile-Time Architecture. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 51](./module-51-binary-data-contracts/index.md) with a **binary layout and range proof** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-51-binary-data-contracts/workbook.md) before observation. The day’s minimum result is: **Define a binary format as a versioned contract rather than a sequence of convenient writes.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Checked Frame Codec](../labs/module-01-checked-frame-codec/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 51 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Define a binary format as a versioned contract rather than a sequence of convenient writes.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 52: Files, Durability, and Transactional Replacement

**Question:** What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?

**Retrieval:** Without notes, restate the invariant carried from Module 51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 52](./module-52-files-durability-and-transactional-replacement/index.md) with a **durability timeline** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-52-files-durability-and-transactional-replacement/workbook.md) before observation. The day’s minimum result is: **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Atomic Archive Store](../labs/module-02-atomic-archive-store/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 52 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 53: Paths, Names, and Platform Boundaries

**Question:** How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

**Retrieval:** Without notes, restate the invariant carried from Module 52 — Files, Durability, and Transactional Replacement. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 53](./module-53-paths-names-and-platform-boundaries/index.md) with a **path threat model** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-53-paths-names-and-platform-boundaries/workbook.md) before observation. The day’s minimum result is: **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Sandboxed Extraction Paths](../labs/module-03-sandboxed-extraction-paths/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 53 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 54: Processes, Environments, and Standard Streams

**Question:** How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?

**Retrieval:** Without notes, restate the invariant carried from Module 53 — Paths, Names, and Platform Boundaries. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 54](./module-54-processes-environments-and-standard-streams/index.md) with a **process boundary contract** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-54-processes-environments-and-standard-streams/workbook.md) before observation. The day’s minimum result is: **Construct commands from a program plus arguments, not an interpolated shell line.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Process Capture](../labs/module-04-bounded-process-capture/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 54 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Construct commands from a program plus arguments, not an interpolated shell line.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 55: Unsafe Rust as a Proof Boundary

**Question:** What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?

**Retrieval:** Without notes, restate the invariant carried from Module 54 — Processes, Environments, and Standard Streams. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 55](./module-55-unsafe-rust-and-safety-proofs/index.md) with a **unsafe obligation ledger** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-55-unsafe-rust-and-safety-proofs/workbook.md) before observation. The day’s minimum result is: **Name the operations Rust requires an unsafe context to perform.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Unsafe Slice Kernel](../labs/module-05-unsafe-slice-kernel/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 55 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Name the operations Rust requires an unsafe context to perform.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Binary Data Contracts: Bytes, Endianness, and Checked Parsing, Files, Durability, and Transactional Replacement, Paths, Names, and Platform Boundaries, Processes, Environments, and Standard Streams, Unsafe Rust as a Proof Boundary** as one dependency chain, rerun the two investigations that changed your model most, and describe the current FrameVault state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 56: Raw Pointers, Provenance, and Uninitialized Memory

**Question:** How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

**Retrieval:** Without notes, restate the invariant carried from Module 55 — Unsafe Rust as a Proof Boundary. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 56](./module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) with a **initialization and provenance map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-56-raw-pointers-provenance-and-uninitialized-memory/workbook.md) before observation. The day’s minimum result is: **Distinguish raw pointers from references and explain why conversion does not transfer ownership.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Panic-Safe Batch Builder](../labs/module-06-panic-safe-batch-builder/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 56 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish raw pointers from references and explain why conversion does not transfer ownership.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 57: Manual Allocation and Owning Unsafe Abstractions

**Question:** How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?

**Retrieval:** Without notes, restate the invariant carried from Module 56 — Raw Pointers, Provenance, and Uninitialized Memory. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 57](./module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) with a **allocator layout record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-57-manual-allocation-and-owning-unsafe-abstractions/workbook.md) before observation. The day’s minimum result is: **Construct and validate `Layout` values without unchecked size arithmetic.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Aligned Byte Buffer](../labs/module-07-aligned-byte-buffer/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 57 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Construct and validate `Layout` values without unchecked size arithmetic.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 58: C FFI: ABI, Strings, Pointers, and Error Boundaries

**Question:** How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

**Retrieval:** Without notes, restate the invariant carried from Module 57 — Manual Allocation and Owning Unsafe Abstractions. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 58](./module-58-c-ffi-abi-strings-and-error-boundaries/index.md) with a **ABI table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-58-c-ffi-abi-strings-and-error-boundaries/workbook.md) before observation. The day’s minimum result is: **Distinguish ABI compatibility from semantic validity and ownership.** Keep one positive case and one causal negative case.

**Laboratory:** Build [C ABI Line Validator](../labs/module-08-c-abi-archive-validator/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 58 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish ABI compatibility from semantic validity and ownership.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 59: Foreign Resources, Callbacks, and Wrapper Architecture

**Question:** How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?

**Retrieval:** Without notes, restate the invariant carried from Module 58 — C FFI: ABI, Strings, Pointers, and Error Boundaries. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 59](./module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) with a **foreign liveness graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-59-foreign-resources-callbacks-and-wrapper-architecture/workbook.md) before observation. The day’s minimum result is: **Separate raw bindings, checked unsafe shims, and safe domain wrappers.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Opaque Foreign Session](../labs/module-09-opaque-foreign-session/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 59 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate raw bindings, checked unsafe shims, and safe domain wrappers.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 60: Integrated Systems Design, Testing, and Audit

**Question:** How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

**Retrieval:** Without notes, restate the invariant carried from Module 59 — Foreign Resources, Callbacks, and Wrapper Architecture. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 60](./module-60-integrated-systems-design-and-audit/index.md) with a **whole-system boundary dossier** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-60-integrated-systems-design-and-audit/workbook.md) before observation. The day’s minimum result is: **Draw one boundary map from external bytes to final effects and back to foreign callers.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Systems Boundary Audit](../labs/module-10-systems-boundary-audit/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 60 in the [FrameVault guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Draw one boundary map from external bytes to final effects and back to foreign callers.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add a bounded archive index to FrameVault while preserving format compatibility, path policy, failure atomicity, allocator safety, and C ABI ownership.**

Seven days later, rebuild the ten-module sequence and the core **whole-system boundary dossier** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
