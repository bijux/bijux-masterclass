# Course 6 Final Review — Rust Systems Programming

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

51. **Binary Data Contracts: Bytes, Endianness, and Checked Parsing** — How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?
52. **Files, Durability, and Transactional Replacement** — What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?
53. **Paths, Names, and Platform Boundaries** — How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?
54. **Processes, Environments, and Standard Streams** — How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?
55. **Unsafe Rust as a Proof Boundary** — What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?
56. **Raw Pointers, Provenance, and Uninitialized Memory** — How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?
57. **Manual Allocation and Owning Unsafe Abstractions** — How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?
58. **C FFI: ABI, Strings, Pointers, and Error Boundaries** — How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?
59. **Foreign Resources, Callbacks, and Wrapper Architecture** — How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?
60. **Integrated Systems Design, Testing, and Audit** — How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a checked packet archive with transactional output, one justified unsafe storage abstraction or a written rejection of it, and a stateless C validation boundary.

Before implementation, write:

```text
product promise and non-goals
owners and authorities
valid and invalid states
success transition
failure, cleanup, and retry state
order and capacity
external assumptions
public API
verification plan
three rejected designs
```

After implementation, preserve six traces: ordinary success, malformed input, rejected state, partial work before failure, cleanup, and one compatibility, platform, scheduler, workload, or peer edge relevant to this course.

## Part 3 — Capstone change

Apply this change to FrameVault:

> Add a bounded archive index to FrameVault while preserving format compatibility, path policy, failure atomicity, allocator safety, and C ABI ownership.

Do not introduce a second source of truth for validation, state, ordering, storage, protocol, scheduling, generation, measurement, or compatibility. Revise the authority map first when the change does not fit the current architecture.

Review the change through:

1. public behavior;
2. owner of the new invariant;
3. state after each failure point;
4. ownership and cleanup;
5. ordering and resource bounds;
6. compatibility or format consequences;
7. independent tests and their limits;
8. the simpler design you rejected.

## Part 4 — Cross-course preservation

Select one guarantee from Course 5 — Rust Metaprogramming and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 6 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **whole-system boundary dossier**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 51 — Binary Data Contracts: Bytes, Endianness, and Checked Parsing:** answer “How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 52 — Files, Durability, and Transactional Replacement:** answer “What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 53 — Paths, Names, and Platform Boundaries:** answer “How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 54 — Processes, Environments, and Standard Streams:** answer “How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 55 — Unsafe Rust as a Proof Boundary:** answer “What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 56 — Raw Pointers, Provenance, and Uninitialized Memory:** answer “How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 57 — Manual Allocation and Owning Unsafe Abstractions:** answer “How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 58 — C FFI: ABI, Strings, Pointers, and Error Boundaries:** answer “How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 59 — Foreign Resources, Callbacks, and Wrapper Architecture:** answer “How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 60 — Integrated Systems Design, Testing, and Audit:** answer “How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of FrameVault: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 6 — Rust Systems Programming is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **whole-system boundary dossier**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
