# Module 98 Workbook — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **claim-to-evidence matrix** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the claim-to-evidence matrix visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — View escape claim

Choose the primary evidence for “a borrowed record view cannot outlive its snapshot.”

### Prediction 2 — Round-trip property

An encoder and decoder share one helper that sorts records. Does `decode(encode(x)) == x` alone prove canonical ordering?

### Prediction 3 — Model independence

The transaction model copies the implementation’s vector update algorithm. Evaluate the evidence.

### Prediction 4 — Miri claim

All `InlineBatch` tests pass under Miri. May the project claim the abstraction is proven sound?

## Part 2 — Diagnose and repair

Each repair must leave a more precise claim-to-evidence matrix. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Test-count dashboard

A release report cites 5,000 passing tests without mapping them to claims.

Required direction: Build a claim matrix and identify uncovered negative API, migration, unsafe, and artifact properties.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the claim-to-evidence matrix changes.

### Repair 2 — Unbounded fuzz target

A parser fuzz target accepts arbitrary declared lengths and allocations.

Required direction: Validate lengths before allocation and cap input, depth, operations, time, and retained corpus.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the claim-to-evidence matrix changes.

### Repair 3 — Only final-state comparison

A model test compares implementation and oracle only after the whole operation sequence.

Required direction: Compare after every prefix so the minimal divergence is visible and later operations cannot accidentally converge.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the claim-to-evidence matrix changes.

## Part 3 — Focused exercises

### Exercise 1 — Compile-fail suite

Protect view escape, retained lending item, and forged witness cases.

Completion standard: Each case fails for one intended cause and records the decisive rule.

### Exercise 2 — Property generator

Generate bounded valid and invalid records for canonical format properties.

Completion standard: Boundary values, Unicode, duplicates, and malformed lengths are represented.

### Exercise 3 — Transition explorer

Enumerate short transaction sequences against an independent map model.

Completion standard: Failures report a minimal sequence and intermediate state.

### Exercise 4 — Unsafe evidence map

Map `InlineBatch` claims to review, destructor tests, state exploration, and Miri.

Completion standard: Every evidence form states its scope and residual risk.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**. Reconstruct its current invariant owner, then decide whether the claim-to-evidence matrix reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — closing a verification gap

AxiomStore currently has unit tests for successful encode/decode, transaction commits, and one legacy migration. The team wants to claim that borrowed views cannot escape, bytes are canonical, failed transactions preserve the old archive, the unsafe batch drops exactly once, old files remain readable, and the CLI never reports success after a failed write.

Build a claim-to-evidence matrix for those six claims. For each row, choose the primary evidence form and at least one complementary form. Include compile-fail contracts, known byte fixtures, property generation, a small independent state model, destructor counters, Miri, process-level tests, and manual unsafe review where appropriate. State what a passing result cannot establish.

Next, find one circular test design. For example, an expected canonical byte vector generated by the same encoder under test, or an oracle that copies the transaction implementation. Replace it with independent evidence. Finally, define resource bounds for fuzzing and model exploration so the verification tool itself cannot turn hostile lengths or unbounded state spaces into denial of service. The output must be a prioritized plan, not a list of every available testing tool.

## Part 4 — Independent laboratory

Build [Model-Checked Log](../../labs/module-08-model-checked-log/README.md) from its `starter/` package.

Build an implementation and independent `BTreeMap` model for a mutation log, then exhaustively compare all bounded operation sequences and preserve minimal counterexamples.

Before implementation, freeze Model-Checked Log’s public behavior and the claim-to-evidence matrix. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Create AxiomStore’s verification matrix covering negative API space, canonical bytes, malformed input, transaction semantics, unsafe drop behavior, old-format fixtures, migration failure, and CLI behavior.

Update AxiomStore’s claim-to-evidence matrix before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, choose the strongest-looking green result in your verification matrix and write three claims it does not establish. Identify one circular oracle you removed or would remove, then add the cheapest independent evidence that can expose the missing failure. Record the resource bounds of the verification tool itself so hostile input cannot turn the test method into an unbounded workload.

## Part 6 — Reconstruct and defend

Given an unseen claim, choose a verification method by its failure model and state what a passing result cannot establish.

Finish without notes by reconstructing the claim-to-evidence matrix. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Model-Checked Log and the AxiomStore increment without seeing your final implementation.
