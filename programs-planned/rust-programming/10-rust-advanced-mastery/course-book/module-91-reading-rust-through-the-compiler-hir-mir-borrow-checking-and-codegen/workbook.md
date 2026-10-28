# Module 91 Workbook — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **source-to-artifact evidence ladder** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the source-to-artifact evidence ladder visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Method resolution before MIR

A type has an inherent `read(&self)` method and implements a trait with `read(&mut self)`. A call uses an immutable binding. Predict the selected method and list the receiver adjustments the compiler must consider before control-flow lowering can explain the body.

### Prediction 2 — Loan ends before lexical block

A mutable reference returned by `Vec::get_mut` is printed and the vector is then pushed within the same block. Predict whether the program compiles when the reference is not used after the print, and identify the access/liveness fact that decides it.

### Prediction 3 — Partial move and drop

Move one field out of a struct whose other field owns a `String`, then leave scope. Predict which values are destroyed and whether a `Drop` implementation on the outer struct changes legality.

### Prediction 4 — Artifact claim

Two generic calls appear as one symbol in an optimized binary. Classify the strongest justified conclusion and the metadata required before comparing another build.

## Part 2 — Diagnose and repair

Each repair must leave a more precise source-to-artifact evidence ladder. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Clone inserted after borrow error

A parser clones its whole input buffer because a returned slice blocks later cursor mutation. Repair the place or lifetime relationship while preserving borrowed output.

Required direction: Shorten the returned borrow, split cursor state from backing storage, or change sequencing. Cloning abandons the intended borrowing contract.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact evidence ladder changes.

### Repair 2 — Runtime experiment used as drop proof

A test prints destructor order and the documentation treats that exact output as the language contract.

Required direction: Derive required destruction from initialization and exit edges. Keep print order as one observation and remove claims that optimization or future toolchains cannot preserve.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact evidence ladder changes.

### Repair 3 — Assembly used to explain a method error

A review begins with assembly to explain why `item.render()` selects the wrong method.

Required direction: Return to resolution: enumerate inherent and trait candidates, autoderef/autoref, and bounds. Machine code exists only after selection succeeds.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the source-to-artifact evidence ladder changes.

## Part 3 — Focused exercises

### Exercise 1 — Receiver adjustment table

Create three types with overlapping inherent and trait methods. For each call, record candidate, adjustment, and fully qualified alternative.

Completion standard: The table predicts every call and does not appeal to source proximity.

### Exercise 2 — Control-flow drop graph

Write a function with `?`, a `match`, partial initialization, and an observable destructor. Draw cleanup on normal and error paths.

Completion standard: Every live value appears exactly once on each applicable exit.

### Exercise 3 — Place projection repair

Diagnose a conflict involving two fields and an indexed element. Produce one API repair that exposes disjointness.

Completion standard: The repair changes places or borrow duration; no blanket cloning is accepted.

### Exercise 4 — Scoped artifact note

Inspect one generic and one dynamic path in a fixed release build.

Completion standard: The note includes semantic parity, build identity, observation, and an explicit expiry condition.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**. Reconstruct its current invariant owner, then decide whether the source-to-artifact evidence ladder reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — one error, four representations

A teammate reports that `collect::<Vec<_>>()` “fails in MIR because the iterator item type is wrong.” The isolated program actually fails during trait selection: a projected iterator item cannot satisfy the requested `FromIterator` goal. After the type error is repaired, a second version compiles but returns records in the wrong order. A release build then shows two large monomorphized helper symbols.

Prepare a three-column evidence notebook. In the first column, record the source-level obligation and the earliest compiler representation capable of deciding it. In the second, record the runtime contract that must be tested independently of compilation. In the third, record artifact observations that are meaningful only for the pinned target, profile, and compiler. Your notebook must explain why an HIR or MIR dump can clarify the program without becoming the language specification, why the ordering defect is not a compiler-phase defect, and why symbol size cannot establish semantic correctness.

Then propose the smallest investigation sequence. It must begin with a minimal source specimen, continue through ordinary compiler diagnostics, use MIR only if control-flow or move elaboration remains unclear, and inspect symbols only after semantic parity is established. End by naming one plausible conclusion that each representation cannot justify.

## Part 4 — Independent laboratory

Build [Compiler Evidence Notebook](../../labs/module-01-compiler-evidence-notebook/README.md) from its `starter/` package.

Build an evidence notebook that classifies claims by phase, records what remains unknown, and includes one drop experiment whose runtime observation is kept separate from the semantic argument.

Before implementation, freeze Compiler Evidence Notebook’s public behavior and the source-to-artifact evidence ladder. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Trace an AxiomStore `RecordView` from snapshot allocation through codec decoding and cursor lending. Separately trace a failed transaction through candidate construction, validation, encoding, temporary-file cleanup, and return. The increment is accepted only when each conclusion names its decisive phase and no artifact observation is presented as a stable language rule.

Update AxiomStore’s source-to-artifact evidence ladder before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

## Part 6 — Reconstruct and defend

Explain a borrow rejection, a destructor obligation, and a code-size observation using three different evidence layers. Then justify why the compiler cannot select the product redesign after the borrow rejection.

Finish without notes by reconstructing the source-to-artifact evidence ladder. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Compiler Evidence Notebook and the AxiomStore increment without seeing your final implementation.
