# Module 100 Solutions — Architectural Synthesis: Building and Defending a Long-Lived Rust System

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Duplicate invariant owner

No single authority exists; legal values can differ by path. Assign structural validity to `Record`, policy to validators, representation checks to codec, and usage shape to CLI.

### Prediction 2 — Advanced mechanism trophy

The unsafe mechanism does not earn its proof cost. Revert to safe storage unless a named product requirement justifies inline fixed capacity.

### Prediction 3 — AXIOM02 unknown version

No. Unknown versions must be rejected explicitly unless a documented compatible extension rule exists.

### Prediction 4 — Aggregate green badge

No. Claims need distinct evidence; a green aggregate can conceal unsupported proof domains.

## Part 2 — Diagnose and repair

Judge every repair against the architecture defense dossier: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Public representation leakage

**Causal defect.** Internal codec structs and unsafe batch fields are exposed to make tests easier.

**Principled repair.** Test through public behavior or crate-private helpers. Keep representation private so evolution remains possible.

A strong answer updates the architecture defense dossier and includes a negative case that fails for the original cause.

### Repair 2 — One error for every failure

**Causal defect.** Usage, validation, capacity, malformed bytes, migration, and I/O all become strings.

**Principled repair.** Restore a typed taxonomy aligned with recovery and stable user reporting.

A strong answer updates the architecture defense dossier and includes a negative case that fails for the original cause.

### Repair 3 — Feature accumulation

**Causal defect.** The final design includes async I/O, plugins, macros, lock-free transactions, and memory mapping because all were taught earlier.

**Principled repair.** Remove every mechanism without a unique requirement. Synthesis is selection and rejection, not feature count.

A strong answer updates the architecture defense dossier and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Invariant ownership map

The construction should answer: Assign every AxiomStore promise to one primary owner.

The decisive acceptance criterion is: No rule is authoritative in two unrelated layers.

Evaluate the result through the architecture defense dossier; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Mechanism subtraction

The construction should answer: Replace one advanced mechanism with a simpler design and compare proof cost.

The decisive acceptance criterion is: The final choice follows product requirements, not course coverage.

Evaluate the result through the architecture defense dossier; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — AXIOM02 transfer

The construction should answer: Add schema tags while preserving AXIOM01 reads and deterministic behavior.

The decisive acceptance criterion is: Compatibility fixtures, migration, CLI, and unknown-version tests all change coherently.

Evaluate the result through the architecture defense dossier; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Architecture defense

The construction should answer: Present product, flows, unsafe dossier, compatibility, evidence, residual risk, and rejected alternatives.

The decisive acceptance criterion is: A fresh reviewer can challenge assumptions and reproduce the reasoning.

Evaluate the result through the architecture defense dossier; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **Architectural Synthesis: Building and Defending a Long-Lived Rust System** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — the mechanism-subtraction council

The GAT codec is justified when callers commonly inspect decoded data without allocating and views must remain tied to snapshot bytes. Const-generic transaction capacity is justified only if distinct capacities are meaningful in type identity and inline storage; otherwise a validated runtime limit plus `Vec` is simpler. Dynamic validators are justified because one future host-selected implementation must coexist with built-ins. `Any` metadata is not justified for ordinary execution; a typed optional capability can be added later. The unsafe inline batch is justified only if measured allocation or representation requirements outweigh its proof burden. Enum dispatch may be useful for closed built-ins but is redundant if the validator registry alone is sufficient. Typestate, a schema macro, async compaction, and a plugin ABI are rejected because the stated product has no staged construction, repetitive schema authority, background service requirement, or cross-language binary extension contract.

A minimal architecture therefore has versioned safe codecs, a borrowed snapshot view, an owned record conversion, a bounded transaction builder, a validator trait-object registry, candidate-first Unix replacement under a documented single-writer filesystem contract, and perhaps the inline batch if its benchmarked benefit is real. Every invariant has one owner.

The unseen owned-snapshot requirement does not invalidate lending reads. Add an explicit owned snapshot type built from validated records; it can be `Send + Sync` when its fields are. Store replacement leaves it independent because it owns data. No pinning, async runtime, or ABI is required.

The proof ledger maps non-escape to compile-fail tests, canonical formats to golden fixtures and properties, transaction behavior to an independent model, unsafe storage to review, destructor tests, and Miri, compatibility to old-version fixtures and MSRV/feature builds, and artifact cost to pinned release inspection. Each mechanism has a removal condition, preventing the final architecture from becoming a museum of advanced features.

## Part 4 — Independent laboratory

A complete [Architecture Council](../../labs/module-10-architecture-council/README.md) satisfies its public contract and makes the architecture defense dossier inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a compact registry architecture, assign every invariant to one owner, and conduct an architecture council that must reject unnecessary mechanisms as well as approve useful ones.

The transfer variant for Architecture Council must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Complete AxiomStore and the independent AXIOM02 extension. Produce the final defense dossier and show that all earlier guarantees—ownership, errors, memory safety, determinism, boundedness, compatibility, and operability—survive the change.

A strong capstone change keeps the responsibility described by the architecture defense dossier local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Defend the system in twenty minutes, including five mechanisms deliberately not used and one residual risk that remains after the complete verification portfolio passes.

The defense passes when it reconstructs the architecture defense dossier from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
