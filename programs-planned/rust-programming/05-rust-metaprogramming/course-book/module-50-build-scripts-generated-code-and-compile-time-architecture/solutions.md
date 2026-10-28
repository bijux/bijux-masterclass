# Reasoned Solutions — Module 50: Build Scripts, Generated Code, and Compile-Time Architecture

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-10-generated-code-build/README.md) · [CommandForge guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 50: Build Scripts, Generated Code, and Compile-Time Architecture**. Compare the reasoning against this question: *How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `case-01/`

- **Outcome:** `compile-pass`
- **Governing rule:** a build script may generate Rust under OUT_DIR.
- **Causal explanation:** The specimen compiles because a build script may generate Rust under OUT_DIR.
- **Principled repair:** retain OUT_DIR generation
- **Weak repair to reject:** write generated files into src

### 2. `case-02/`

- **Outcome:** `compile-fail`
- **Governing rule:** build input validation may stop compilation before crate compilation.
- **Causal explanation:** The compiler rejects the specimen because build input validation may stop compilation before crate compilation.
- **Principled repair:** fix the checked input
- **Weak repair to reject:** silently keep the last row

### 3. `case-03/`

- **Outcome:** `compile-pass`
- **Governing rule:** rerun-if-changed can declare the precise external input.
- **Causal explanation:** The specimen compiles because rerun-if-changed can declare the precise external input.
- **Principled repair:** retain explicit change tracking
- **Weak repair to reject:** scan the entire source tree

### 4. `case-04/`

- **Outcome:** `compile-fail`
- **Governing rule:** include paths must name a file actually generated in OUT_DIR.
- **Causal explanation:** The compiler rejects the specimen because include paths must name a file actually generated in OUT_DIR.
- **Principled repair:** make output and include contract agree
- **Weak repair to reject:** commit a stale generated file into src

### 5. `case-05/`

- **Outcome:** `compile-pass`
- **Governing rule:** generated output can preserve deterministic sorted order.
- **Causal explanation:** The specimen compiles because generated output can preserve deterministic sorted order.
- **Principled repair:** retain canonical ordering
- **Weak repair to reject:** use filesystem or hash iteration order

### 6. `case-06/`

- **Outcome:** `compile-fail`
- **Governing rule:** build scripts should reject malformed checked input.
- **Causal explanation:** The compiler rejects the specimen because build scripts should reject malformed checked input.
- **Principled repair:** repair the input schema
- **Weak repair to reject:** skip malformed rows silently

### 7. `case-07/`

- **Outcome:** `compile-pass`
- **Governing rule:** build scripts may expose compile-time constants through included Rust.
- **Causal explanation:** The specimen compiles because build scripts may expose compile-time constants through included Rust.
- **Principled repair:** retain a small generated surface
- **Weak repair to reject:** parse the same config again at runtime

### 8. `case-08/`

- **Outcome:** `compile-fail`
- **Governing rule:** a build script process failure prevents package compilation.
- **Causal explanation:** The compiler rejects the specimen because a build script process failure prevents package compilation.
- **Principled repair:** satisfy the validation rule
- **Weak repair to reject:** catch and ignore the build failure

## How to review the compiler specimens

The machine-readable outcomes are in [`compiler-labs/manifest.json`](../../compiler-labs/manifest.json). For **build reproducibility and source authority**, compare your prediction against five questions:

1. Which checked-in input is authoritative, and is every generated artifact derived solely from it?
2. Are all files and environment variables that affect output declared through precise Cargo rerun directives?
3. Does validation report physical source positions and reject duplicates before code generation?
4. Is output byte-for-byte deterministic under identical inputs and independent of hash iteration order?
5. Is generated code written only under `OUT_DIR` and replaced after a complete, flushed candidate is available?

Diagnostic prose may change between compiler releases. The isolated source shape and governing phase are the durable evidence.

## Broken-design repair

**Step 1.** Name one checked-in external input and one generated output under `OUT_DIR`. Never modify source files from `build.rs`.

**Step 2.** Emit precise `cargo::rerun-if-changed` and `cargo::rerun-if-env-changed` instructions for declared inputs only.

**Step 3.** Parse and validate the complete input before writing. Detect duplicates, malformed rows, invalid ranges, and nondeterministic order.

**Step 4.** Generate to a temporary in-memory buffer or temporary file, then write one deterministic output with no timestamps, absolute paths, or host-only assumptions.

**Step 5.** Remove overlapping authority. If exit codes come from the external table, no macro or runtime module independently redeclares them.

The repaired design should make **build reproducibility and source authority** smaller and more inspectable than the broken proposal. Judge it by whether one declaration owns the mechanical relationship, the expanded Rust remains readable, and each invalid input fails in the earliest phase that possesses the necessary information.

## Exercise reasoning

### Exercise 1 — Host versus target

The build script itself is compiled for and runs on the host, so `cfg!` describes the host. Target configuration is supplied through Cargo environment variables such as `CARGO_CFG_TARGET_OS`. Generated target-specific code must use the declared target information.

### Exercise 2 — Rerun contract

Emit `cargo::rerun-if-changed=config/codes.tsv` and `cargo::rerun-if-env-changed=COMMAND_PREFIX`. Also avoid reading undeclared files or environment variables. Precise triggers improve incremental correctness and explain inputs.

### Exercise 3 — OUT_DIR discipline

It mutates the source tree during compilation, creates races, dirty working directories, confusing editor state, and packaging differences. Cargo provides `OUT_DIR` as the build-owned output location; source includes it through `include!(concat!(env!("OUT_DIR"), "/generated.rs"))`.

### Exercise 4 — Transactional generation

Read and validate all rows into a normalized model, render the complete output in memory, then write the final `OUT_DIR` file only after success. If any error occurs, print a clear Cargo error or return failure without replacing a previously valid output. Do not stream half-validated rows directly into the final file.

### Exercise 5 — Deterministic input

Declare the directory or exact files as inputs, collect paths, normalize them, sort by a documented key, reject duplicates, read with explicit encoding assumptions, and never depend on filesystem iteration order. Better still, use one manifest that defines order explicitly.

### Exercise 6 — Authority review

The DSL may reference handler metadata but must not redeclare handler signatures or argument fields. The build script may generate exit-code constants but must not assign diagnostic codes already owned by the diagnostic macro. References are allowed; independent declarations of the same fact are not.

## Reference implementation comparison

The reference implementation is in [`labs/module-10-generated-code-build/solution`](../../labs/module-10-generated-code-build/solution). Review it in this order:

1. rebuild on every authoritative input change;
2. deterministic output independent of hash-map order or timestamps;
3. line-aware malformed-input errors;
4. no checked-in copy competing with `OUT_DIR` output;

Keep your implementation when its **build reproducibility and source authority** contract is at least as precise with a clearer or smaller design. Revise it when the reference exposes an accepted input, failure phase, generated-name rule, evaluation effect, or determinism obligation missing from your tests.

## Capstone review

For the Module 50 increment, a strong result demonstrates **designing deterministic compile-time architecture across macros, build scripts, external inputs, generated files, and runtime code**. The capstone should still read primarily as ordinary Rust. Generated surfaces must be compact enough to inspect through tests or expansion tools, and runtime domain behavior must remain callable without understanding macro internals.

## What a strong explanation includes

A strong defense of this module explains:

- what Cargo knows from rerun directives;
- why generated output belongs under `OUT_DIR`;
- how partial output is prevented;
- which generated interface must remain stable for downstream Rust;
- how the generated ordinary Rust can be inspected and tested without trusting the generator blindly;
- which simpler non-macro design was considered and why it is insufficient for this exact source-of-truth relationship.

## Deep reasoning and transfer

### Decisive model

> How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

Build a **generation authority and reproducibility record**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Explain the Cargo build-script lifecycle and communication protocol.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Read host and target configuration correctly.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Declare rebuild inputs with `cargo::rerun-if-changed` and `cargo::rerun-if-env-changed`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Write generated files only under `OUT_DIR`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Validate external data before emitting Rust.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Explain the Cargo build-script lifecycle and communication protocol.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the generation authority and reproducibility record.

### Laboratory transfer review

For [Generated Code Build](../../labs/module-10-generated-code-build/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In CommandForge, Module 50 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Build Scripts, Generated Code, and Compile-Time Architecture**, which relationship decides this question: “How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to CommandForge?
