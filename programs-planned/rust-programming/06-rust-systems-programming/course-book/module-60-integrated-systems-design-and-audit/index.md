# 60 — Integrated Systems Design, Testing, and Audit

**Course 6, day 10 · Module 60 of 90**  
`████████████████████` **60/90**

[← Module 59: Foreign Resources, Callbacks, and Wrapper Architecture](../module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) · [Course 6 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Program progress](../../../PROGRESS.md)

## The question

> How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

## Why this comes now

The final module does not add another low-level trick. It integrates the ten-day system and asks whether every external input, resource transition, unsafe claim, and foreign contract has a visible owner. FrameVault becomes the test case, but the review method transfers to databases, media tools, runtimes, storage engines, and language bindings.

## What you will be able to do

- Draw one boundary map from external bytes to final effects and back to foreign callers.
- Build a threat model that separates malformed input, hostile namespaces, untrusted processes, allocation pressure, and invalid foreign callers.
- Use layered tests, dynamic tools, cross-target checks, and failure injection as complementary evidence.
- Audit unsafe code through invariants and call graphs rather than counting blocks.
- Define deterministic output, compatibility, and recovery rules as product contracts.
- Defend exclusions and future-course boundaries rather than pretending to solve every systems problem.

## Core model

### Start with the boundary map

FrameVault has five external boundaries:

```text
archive bytes ↔ codec
filesystem namespace ↔ store and extraction policy
child process ↔ capture adapter
raw allocation ↔ AlignedBytes safe owner
C caller ↔ exported ABI and opaque sessions
```

Each boundary needs an input model, validation, ownership transition, error model, and effect. Draw arrows in both directions. For example, extraction consumes a validated logical path and payload, but emits a host path and file side effect. The path policy and file protocol must both hold; neither can compensate for the other.

### Threat models are mechanism-specific

Classify threats instead of writing “input may be malicious”:

- **Malformed archive** — truncation, overflow, invalid names, checksum mismatch, duplicate names, huge declared lengths.
- **Host namespace** — symlinks, reparse points, races, permission changes, preexisting files, non-Unicode names.
- **Child process** — unbounded runtime, huge output, inherited secrets, executable substitution, unusual argument parsing.
- **Allocation** — exhaustion, invalid layout, size overflow.
- **Foreign caller** — null misuse, dangling pointers, wrong lengths, double free, callback retention, reentrancy.
- **Compatibility** — unknown versions, flags, entry kinds, changed ABI, changed error codes.

Then state which are prevented, detected, bounded, documented, or outside the current product.

### Tests should mirror the contract layers

A complete suite has distinct layers:

1. pure codec unit tests;
2. golden byte vectors for stable format encoding;
3. truncation tests at every byte boundary;
4. malformed-length and limit tests;
5. filesystem integration tests in fresh temporary directories;
6. path traversal and symlink-policy tests where supported;
7. process tests using the current executable as a deterministic child;
8. unsafe-abstraction tests for empty, aligned, mutable, and drop states;
9. Rust-side ABI tests calling exported functions through raw pointers;
10. external C smoke tests on prepared CI targets;
11. CLI process tests for status and output.

A passing end-to-end test cannot reveal which contract is missing. Layered tests localize evidence.

### Negative space deserves tests

Systems correctness often lives in what must not happen:

- no allocation before declared lengths pass limits;
- no destination truncation before the commit point;
- no parent or absolute extraction component;
- no shell invocation;
- no unsafe decoder for ordinary file fields;
- no public raw pointer in the safe API;
- no panic across FFI;
- no callback pointer retention;
- no duplicate free;
- no ignored trailing bytes.

Turn these into compiler cases, API shape checks, source policy checks, and adversarial tests.

### Miri, sanitizers, fuzzing, and interpreters answer different questions

Run Miri over focused unsafe abstractions and FFI tests where supported. Use AddressSanitizer or similar tools on native test binaries to catch out-of-bounds and lifetime errors not modeled identically by every interpreter. Fuzz the codec with arbitrary bytes and the logical-path parser with hostile strings. Use mutation tests or deliberately broken variants to verify that the suite detects missing checks.

No one tool proves soundness. Miri explores executed Rust paths under its model; sanitizers instrument target executions; fuzzing searches input space; static review proves invariants over all valid states. Record tool versions and targets because results are environment-dependent.

### Cross-platform testing is part of the specification

At minimum, test supported Unix and Windows targets for:

- path prefixes and separators;
- non-Unicode or non-scalar-value names where the target permits them;
- replacement behavior and file sharing;
- process argument boundaries;
- exit-status representation;
- C ABI compilation and symbol export;
- pointer width and endianness assumptions.

A Linux-only passing suite does not prove a cross-platform path or process claim. If only one target is supported, say so and remove false portability language.

### Determinism needs an explicit ordering policy

FrameVault sorts packed logical names by their UTF-8 byte representation, preserves command argument order, preserves archive entry order, and emits fields in a fixed little-endian format. It never relies on directory iteration or hash-map order.

Timestamps are excluded from the version 1 archive so identical inputs produce identical bytes. A later metadata extension must define normalization if reproducibility remains a goal.

### Compatibility is a reader and writer contract

A versioned format needs rules for:

- unknown version;
- unknown entry kind;
- unknown flag bits;
- duplicate logical names;
- trailing bytes;
- reserved fields;
- maximum sizes;
- canonical writer output.

A C ABI needs symbol versions or release policy, stable integer codes, struct extension strategy, and ownership compatibility. “We can change it later” is not a design. Course 3’s API evolution principles now apply to bytes and symbols.

### Audit unsafe code through reachable safe behavior

List every safe public function that can reach an unsafe block. For each, prove that its validation and private invariants establish the unsafe preconditions. Then inspect every mutation and destructor that can invalidate the invariant.

Counted unsafe lines are a useful trend, not a soundness argument. One line constructing a slice can be unsound through a bad lifetime; a longer allocator implementation can be sound with a complete invariant. Review quality depends on proof precision.

### A systems product needs operational errors

Errors should retain:

- operation;
- path, command, entry, or symbol involved;
- byte offset where relevant;
- declared and allowed sizes;
- underlying `io::Error` source;
- foreign status code;
- whether the previous durable value remains intact.

Avoid one giant string error. Typed layers can convert upward while preserving sources and structured fields. CLI rendering is the final boundary.

### Know which problems belong to later courses

FrameVault deliberately does not provide concurrent packing, asynchronous process streaming, memory-mapped files, cryptographic signatures, high-performance zero-copy indexing, or a production sandbox. Course 7 covers threads and atomics, Course 8 async and networking, and Course 9 measurement, security hardening, packaging, and production operations.

A disciplined course successor preserves those future learning boundaries. The final design is complete for its stated contract, not universal.

### The final defense is a proof narrative

A strong defense proceeds in causal order:

1. state the archive and ABI contracts;
2. show where every untrusted length is bounded;
3. identify the filesystem commit point;
4. state extraction assumptions;
5. preserve process argument and stream boundaries;
6. recite the `AlignedBytes` invariant;
7. map every unsafe operation to its evidence;
8. trace C ownership and callback lifetimes;
9. show deterministic ordering and version rejection;
10. identify remaining target-dependent claims.

If the explanation depends on “Rust probably handles that,” the boundary has not been understood.

### FrameVault final architecture

```text
CLI arguments (OsString)
    ↓ app parser
Create / List / Verify / Extract / Capture
    ↓
archive model ←→ safe binary codec ←→ archive bytes
    ↓                    ↓
path policy          AlignedBytes optional staging
    ↓                    ↓
transactional store     small audited unsafe core
    ↓
filesystem

archive model ←→ C ABI validator / opaque session
                    ↓
                foreign caller

capture request → Command → child output bytes → command entry
```

Every arrow has one representation conversion. There is no direct file-byte-to-struct cast, no shell line, no lossy host-path identity, and no public raw allocator pointer.

### Final invariant register

| Component | Invariant |
|---|---|
| codec cursor | offset equals consumed prefix; failure does not advance |
| archive model | names are unique valid logical paths; counts and totals fit limits |
| store | destination is untouched before successful replacement |
| extraction | each logical component is normal; destination tree satisfies stated no-link assumption |
| process capture | program and arguments remain separate; streams remain bytes; stored output fits format limits |
| aligned owner | zero state has no allocation; nonzero state uniquely owns one exact-layout initialized byte range |
| validator ABI | out report is initialized before return; no panic or Rust reference crosses boundary |
| opaque session | one successful open creates one release obligation; enumeration only borrows |
| callback | synchronous and non-retaining; context remains live for call |

A code review should be able to locate the constructor and mutation points that preserve each row.

### Compatibility table

Version 1 rejects unknown magic, entry kinds, nonzero flags, duplicate names, oversized fields, and trailing bytes. This is intentionally strict. Future readers may add a version dispatch that preserves the old parser unchanged. Future writers should continue to emit canonical version 1 only when explicitly requested.

The C ABI treats symbol removal, signature changes, status-code reinterpretation, and `repr(C)` report-size changes as breaking. Adding a new function or a previously unused status code can be compatible when old callers need not understand it.

### Release proof route

A prepared machine should run:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --doc
cargo build --release
python3 ../tools/run_compiler_labs.py 06-rust-systems-programming
cargo +nightly miri test --manifest-path capstone/Cargo.toml
```

Miri availability and nightly version are recorded rather than hidden. Platform CI runs on at least one Unix and one Windows target. A C smoke consumer is compiled where a C compiler exists. Archive golden fixtures are compared byte for byte.

### Independent final change

A useful final assessment is to add an optional comment entry kind without weakening version behavior. You must:

- assign a new kind value;
- specify payload and name rules;
- update encoder and decoder symmetrically;
- decide whether extraction ignores or materializes it;
- expose it through list and FFI enumeration;
- preserve old unknown-kind rejection in a version 1 compatibility branch or deliberately version the format;
- add golden, truncation, and ABI tests.

This change crosses representation, model, CLI, and foreign surfaces. It tests whether the architecture is understood rather than copied.

## Use the idea in a complete program

FrameVault is completed as a library, CLI, and C-compatible library. The final increment adds golden-format fixtures, exhaustive truncation tests, path-adversary tests, deterministic self-child process capture, aligned-buffer tests, ABI session tests, a safety dossier, a compatibility table, and a demonstration script. The CLI supports create, list, verify, extract, capture, help, and version.

The matching independent laboratory is [Systems Boundary Audit](../../labs/module-10-systems-boundary-audit/README.md). It isolates the mechanism so you can test the proof without carrying the whole capstone in your head.

## Practice sequence

Complete the [workbook](workbook.md) without consulting earlier chapters, then build the Systems Boundary Audit lab against an unseen defect set. Walk FrameVault in external-input order—bytes, pathnames, process state, allocation, ABI, cleanup—and require every guarantee to point to code, a test, target evidence, or an explicit limitation.

## Ready to continue

You are ready to complete Course 6 when you can defend FrameVault boundary by boundary, identify claims that depend on target evidence, repair an unseen unsafe or I/O defect without weakening the product, and implement an independent binary utility under the same proof discipline.

## Primary Rust references

- [Rust Reference: undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)
- [Rustonomicon](https://doc.rust-lang.org/nomicon/)
- [Miri repository and guide](https://github.com/rust-lang/miri)
- [Rust standard library](https://doc.rust-lang.org/std/)

## Continue

1. Complete the [Module 60 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 60 — Systems Boundary Audit](../../labs/module-10-systems-boundary-audit/README.md) from its public contract.
3. Apply the Module 60 increment in the [FrameVault engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
