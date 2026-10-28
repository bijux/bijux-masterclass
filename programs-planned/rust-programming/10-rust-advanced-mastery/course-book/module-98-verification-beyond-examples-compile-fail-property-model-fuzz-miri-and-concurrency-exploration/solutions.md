# Module 98 Solutions — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

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

A strong answer updates the claim-to-evidence matrix and includes a negative case that fails for the original cause.

### Repair 2 — Unbounded fuzz target

**Causal defect.** A parser fuzz target accepts arbitrary declared lengths and allocations.

**Principled repair.** Validate lengths before allocation and cap input, depth, operations, time, and retained corpus.

A strong answer updates the claim-to-evidence matrix and includes a negative case that fails for the original cause.

### Repair 3 — Only final-state comparison

**Causal defect.** A model test compares implementation and oracle only after the whole operation sequence.

**Principled repair.** Compare after every prefix so the minimal divergence is visible and later operations cannot accidentally converge.

A strong answer updates the claim-to-evidence matrix and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Compile-fail suite

The construction should answer: Protect view escape, retained lending item, and forged witness cases.

The decisive acceptance criterion is: Each case fails for one intended cause and records the decisive rule.

Evaluate the result through the claim-to-evidence matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Property generator

The construction should answer: Generate bounded valid and invalid records for canonical format properties.

The decisive acceptance criterion is: Boundary values, Unicode, duplicates, and malformed lengths are represented.

Evaluate the result through the claim-to-evidence matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Transition explorer

The construction should answer: Enumerate short transaction sequences against an independent map model.

The decisive acceptance criterion is: Failures report a minimal sequence and intermediate state.

Evaluate the result through the claim-to-evidence matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Unsafe evidence map

The construction should answer: Map `InlineBatch` claims to review, destructor tests, state exploration, and Miri.

The decisive acceptance criterion is: Every evidence form states its scope and residual risk.

Evaluate the result through the claim-to-evidence matrix; helper names may differ, but the invariant owner and adversarial case must be explicit.

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
