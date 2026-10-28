# Laboratory 97 — Dispatch Observatory

**Course 10 · Module 97: From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size**

[Chapter](../../course-book/module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) · [Workbook](../../course-book/module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size**: How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design? The product must make **Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **source-to-artifact observation** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build three semantically equivalent execution paths for one scoring workload: generic static dispatch, a closed enum, and a trait object. The laboratory’s product is not a benchmark winner. It is a reproducible observatory that separates semantic parity, architectural openness, and artifact-specific cost.

The starter contains one static path. Add at least two scorer implementations, an enum covering the closed built-in set, and a `dyn Score` path that can store a runtime-selected scorer.

### Semantic oracle

Before measuring anything, define one range of inputs and assert that all three paths produce the same result for every input and scorer. Include overflow policy rather than relying on debug-versus-release behavior. If arithmetic can fail, make that failure part of the common contract.

### Artifact record

Create a small report format that records:

- toolchain and target;
- Cargo profile and features;
- source revision or package version;
- number and distribution of calls;
- semantic parity result;
- binary or section size when measured;
- latency or throughput when measured;
- limitations of the observation.

The Rust library should produce deterministic workload inputs and results. Shell commands for symbol or size inspection belong in the README or a script, not inside the semantic oracle.

### Decision problem

Assume built-in scorers are closed and frequently called, while external scorers are host-selected and heterogeneous. Propose a hybrid architecture. Explain why one mechanism need not dominate the entire product. Then change the requirement: the deployed target has a strict flash budget but loose latency requirements. State what new artifact evidence could justify erasing the built-ins.

### Counterexamples

Reject at least these weak conclusions:

- fewer source lines means smaller machine code;
- generic code is always faster;
- trait objects are always smaller;
- one debug benchmark determines a release architecture;
- symbol size proves semantic equivalence.

### Transfer

Repeat the observatory with a larger scorer whose implementation dominates call overhead. Predict how that changes the relative importance of dispatch, then measure under the same profile when a Rust toolchain is available.

### Using the reference

Inspect `solution/` after your parity suite is complete. The reference is intentionally small and provides no credible performance result by itself. Compare semantic boundaries and extension authority; retain your own measurement dossier.

### Mechanism-specific completion standard

You can choose dispatch from openness and caller requirements, establish parity before measurement, and label every size or speed conclusion with its artifact scope. A benchmark table without a variation map is incomplete.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Dispatch Observatory**.
2. Draw the smallest **source-to-artifact observation** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.
- Compare static dispatch, enum dispatch, and trait-object dispatch through behavior, extension model, call shape, and measured artifact cost.
- Inspect symbols, section sizes, assembly, and layout observations for one pinned target and profile without claiming portability.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 97 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **source-to-artifact observation**. Defend why your design is simpler than one plausible alternative under the new requirements.
