# Laboratory 7 — Dispatch Observatory

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can choose dispatch from openness and caller requirements, establish parity before measurement, and label every size or speed conclusion with its artifact scope. A benchmark table without a variation map is incomplete.
