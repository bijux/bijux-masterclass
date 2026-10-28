# Workbook — Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

[Chapter](index.md) · [Laboratory](../../labs/module-08-model-checked-log/README.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration** has become a usable model rather than remembered vocabulary. Its governing question is: *Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?* Preserve your first prediction and record decisive facts in a **verification claim matrix**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?**
3. Draw the smallest **verification claim matrix** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

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

For **Repair 2 — Unbounded fuzz target**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the claim-to-evidence matrix changes.

### Repair 3 — Only final-state comparison

A model test compares implementation and oracle only after the whole operation sequence.

Required direction: Compare after every prefix so the minimal divergence is visible and later operations cannot accidentally converge.

For **Repair 3 — Only final-state comparison**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the claim-to-evidence matrix changes.

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

Choose one artifact from Courses 1–10 and reassess it through **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**. Reconstruct its current invariant owner, then decide whether the claim-to-evidence matrix reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.

### Applied case study — closing a verification gap

AxiomStore currently has unit tests for successful encode/decode, transaction commits, and one legacy migration. The team wants to claim that borrowed views cannot escape, bytes are canonical, failed transactions preserve the old archive, the unsafe batch drops exactly once, old files remain readable, and the CLI never reports success after a failed write.

Build a claim-to-evidence matrix for those six claims. For each row, choose the primary evidence form and at least one complementary form. Include compile-fail contracts, known byte fixtures, property generation, a small independent state model, destructor counters, Miri, process-level tests, and manual unsafe review where appropriate. State what a passing result cannot establish.

Next, find one circular test design. For example, an expected canonical byte vector generated by the same encoder under test, or an oracle that copies the transaction implementation. Replace it with independent evidence. Finally, define resource bounds for fuzzing and model exploration so the verification tool itself cannot turn hostile lengths or unbounded state spaces into denial of service. The output must be a prioritized plan, not a list of every available testing tool.

### Interleaved reasoning pass

1. For **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the verification claim matrix.
2. For **Select compile-fail tests, examples, properties, model exploration, fuzzing, Miri, schedule exploration, or benchmarks according to the claim**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the verification claim matrix.
3. For **Write generators and shrinkable models that preserve domain validity while reaching boundary and failure states**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the verification claim matrix.
4. For **Construct a small reference model and compare implementation traces after every operation rather than only final output**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the verification claim matrix.

5. Identify one guarantee from an earlier course that a careless implementation of **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Model-Checked Log](../../labs/module-08-model-checked-log/README.md) from its `starter/` package.

Build an implementation and independent `BTreeMap` model for a mutation log, then exhaustively compare all bounded operation sequences and preserve minimal counterexamples.

Before implementation, freeze Model-Checked Log’s public behavior and the claim-to-evidence matrix. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

### Laboratory acceptance trace

Before opening the reference implementation for **Model-Checked Log**, record:

- the public behavior that demonstrates **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create AxiomStore’s verification matrix covering negative API space, canonical bytes, malformed input, transaction semantics, unsafe drop behavior, old-format fixtures, migration failure, and CLI behavior.

Update AxiomStore’s claim-to-evidence matrix before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, choose the strongest-looking green result in your verification matrix and write three claims it does not establish. Identify one circular oracle you removed or would remove, then add the cheapest independent evidence that can expose the missing failure. Record the resource bounds of the verification tool itself so hostile input cannot turn the test method into an unbounded workload.

### Capstone invariant trace

For the Module 98 AxiomStore increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Given an unseen claim, choose a verification method by its failure model and state what a passing result cannot establish.

Finish without notes by reconstructing the claim-to-evidence matrix. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Model-Checked Log and the AxiomStore increment without seeing your final implementation.

### Closed-book defense

In five minutes, answer “Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?” using the **verification claim matrix**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside AxiomStore. A list of APIs without the deciding relationship is incomplete.
