# Reasoned Solutions — Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-model-checked-log/README.md) · [AxiomStore guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 98: Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**. Compare the reasoning against this question: *Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction

### Prediction 1 — View escape claim

A compile-fail contract directly exercises the negative type relationship. Runtime tests cannot execute an illegal program.

### Prediction 2 — Round-trip property

Not fully; shared logic can mask defects. Add known vectors, a separately stated canonical-order property, and invalid noncanonical inputs.

### Prediction 3 — Model independence

The model can reproduce the same bug. Use a simpler independent representation such as `BTreeMap` and compare after every prefix.

### Prediction 4 — Miri claim

No. Miri checks executed paths under its model. Review, state modeling, panic cases, and unexecuted generic behaviors remain relevant.

## Part 2 — Diagnose and repair

Judge every repair against the claim-to-evidence matrix: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Test-count dashboard

**Causal defect.** A release report cites 5,000 passing tests without mapping them to claims.

**Principled repair.** Build a claim matrix and identify uncovered negative API, migration, unsafe, and artifact properties.

The negative case should reintroduce **Test-count dashboard** while preserving the surrounding requirement. The claim-to-evidence matrix must identify the first phase at which the original assumption becomes invalid.

### Repair 2 — Unbounded fuzz target

**Causal defect.** A parser fuzz target accepts arbitrary declared lengths and allocations.

**Principled repair.** Validate lengths before allocation and cap input, depth, operations, time, and retained corpus.

The negative case should reintroduce **Unbounded fuzz target** while preserving the surrounding requirement. The claim-to-evidence matrix must identify the first phase at which the original assumption becomes invalid.

### Repair 3 — Only final-state comparison

**Causal defect.** A model test compares implementation and oracle only after the whole operation sequence.

**Principled repair.** Compare after every prefix so the minimal divergence is visible and later operations cannot accidentally converge.

The negative case should reintroduce **Only final-state comparison** while preserving the surrounding requirement. The claim-to-evidence matrix must identify the first phase at which the original assumption becomes invalid.

## Part 3 — Focused exercises

### Exercise 1 — Compile-fail suite

The construction should answer: Protect view escape, retained lending item, and forged witness cases.

The decisive acceptance criterion is: Each case fails for one intended cause and records the decisive rule.

For **Compile-fail suite**, apply the claim-to-evidence matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 2 — Property generator

The construction should answer: Generate bounded valid and invalid records for canonical format properties.

The decisive acceptance criterion is: Boundary values, Unicode, duplicates, and malformed lengths are represented.

For **Property generator**, apply the claim-to-evidence matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 3 — Transition explorer

The construction should answer: Enumerate short transaction sequences against an independent map model.

The decisive acceptance criterion is: Failures report a minimal sequence and intermediate state.

For **Transition explorer**, apply the claim-to-evidence matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 4 — Unsafe evidence map

The construction should answer: Map `InlineBatch` claims to review, destructor tests, state exploration, and Miri.

The decisive acceptance criterion is: Every evidence form states its scope and residual risk.

For **Unsafe evidence map**, apply the claim-to-evidence matrix to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Cross-course transfer

Full credit may conclude that **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.

### Applied case study — closing a verification gap

The non-escape claim is primarily protected by compile-fail documentation or a dedicated negative crate; runtime tests cannot execute the forbidden program. Canonical bytes need checked-in known vectors and a property such as decode-then-reencode equality, with the caveat that shared helper logic can mask defects. Failure atomicity needs process or filesystem tests that compare the preexisting bytes after injected pre-commit failures, complemented by a small transaction model. Exactly-once destruction needs destructor counters across push, pop, clear, drop, and panic paths; Miri and review complement but do not replace those tests. Compatibility needs immutable old-version fixtures and migration tests. CLI exit truth requires process-level tests that inspect status, stdout, stderr, and final file state.

A circular canonical test calls the production encoder to create its own expected bytes. Replace it with a hand-authored or independently generated fixture whose fields and checksum are documented. A circular transaction oracle uses the same vector mutation algorithm; replace it with a `BTreeMap` model and compare after every operation prefix.

Fuzz targets must cap input length before allocation and bound declared record lengths, operation count, nesting, runtime, and retained corpus. Model exploration must use a finite operation alphabet, key/value domain, and depth, and report the shortest divergent prefix.

Passing evidence remains scoped. Compile-fail tests protect the compiled API form, not future edits. Miri covers executed paths under its model. Fixtures cover known versions, not every future migration. The plan should prioritize causal negative API tests, canonical fixtures, and failure-state preservation before adding broad randomized volume.

## Part 4 — Independent laboratory

A complete [Model-Checked Log](../../labs/module-08-model-checked-log/README.md) satisfies its public contract and makes the claim-to-evidence matrix inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build an implementation and independent `BTreeMap` model for a mutation log, then exhaustively compare all bounded operation sequences and preserve minimal counterexamples.

The transfer variant for Model-Checked Log must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Create AxiomStore’s verification matrix covering negative API space, canonical bytes, malformed input, transaction semantics, unsafe drop behavior, old-format fixtures, migration failure, and CLI behavior.

A strong capstone change keeps the responsibility described by the claim-to-evidence matrix local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Given an unseen claim, choose a verification method by its failure model and state what a passing result cannot establish.

The defense passes when it reconstructs the claim-to-evidence matrix from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.

## Deep reasoning and transfer

### Decisive model

> Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?

Build a **verification claim matrix**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Select compile-fail tests, examples, properties, model exploration, fuzzing, Miri, schedule exploration, or benchmarks according to the claim.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Write generators and shrinkable models that preserve domain validity while reaching boundary and failure states.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Construct a small reference model and compare implementation traces after every operation rather than only final output.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Interpret a clean tool run as evidence for executed cases rather than universal proof.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the verification claim matrix.

### Reference implementation comparison

For [Model-Checked Log](../../labs/module-08-model-checked-log/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In AxiomStore, Module 98 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**, which relationship decides this question: “Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to AxiomStore?
