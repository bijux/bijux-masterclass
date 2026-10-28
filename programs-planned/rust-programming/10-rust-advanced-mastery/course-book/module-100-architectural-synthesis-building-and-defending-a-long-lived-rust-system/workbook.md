# Module 100 Workbook — Architectural Synthesis: Building and Defending a Long-Lived Rust System

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **architecture defense dossier** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the architecture defense dossier visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Duplicate invariant owner

Record validation appears in `Record::new`, validators, codec decode, and CLI parsing with different rules. Predict the maintenance failure.

### Prediction 2 — Advanced mechanism trophy

AxiomStore replaces `Vec<Operation>` with unsafe inline storage but has no fixed-capacity or measured representation requirement. Evaluate the decision.

### Prediction 3 — AXIOM02 unknown version

A reader sees `AXIOM03`. Should it attempt AXIOM02 decoding because the header is similar?

### Prediction 4 — Aggregate green badge

All tests pass, but no negative view-lifetime, migration, unsafe, or MSRV evidence is recorded. Is release evidence complete?

## Part 2 — Diagnose and repair

Each repair must leave a more precise architecture defense dossier. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Public representation leakage

Internal codec structs and unsafe batch fields are exposed to make tests easier.

Required direction: Test through public behavior or crate-private helpers. Keep representation private so evolution remains possible.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the architecture defense dossier changes.

### Repair 2 — One error for every failure

Usage, validation, capacity, malformed bytes, migration, and I/O all become strings.

Required direction: Restore a typed taxonomy aligned with recovery and stable user reporting.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the architecture defense dossier changes.

### Repair 3 — Feature accumulation

The final design includes async I/O, plugins, macros, lock-free transactions, and memory mapping because all were taught earlier.

Required direction: Remove every mechanism without a unique requirement. Synthesis is selection and rejection, not feature count.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the architecture defense dossier changes.

## Part 3 — Focused exercises

### Exercise 1 — Invariant ownership map

Assign every AxiomStore promise to one primary owner.

Completion standard: No rule is authoritative in two unrelated layers.

### Exercise 2 — Mechanism subtraction

Replace one advanced mechanism with a simpler design and compare proof cost.

Completion standard: The final choice follows product requirements, not course coverage.

### Exercise 3 — AXIOM02 transfer

Add schema tags while preserving AXIOM01 reads and deterministic behavior.

Completion standard: Compatibility fixtures, migration, CLI, and unknown-version tests all change coherently.

### Exercise 4 — Architecture defense

Present product, flows, unsafe dossier, compatibility, evidence, residual risk, and rejected alternatives.

Completion standard: A fresh reviewer can challenge assumptions and reproduce the reasoning.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Architectural Synthesis: Building and Defending a Long-Lived Rust System**. Reconstruct its current invariant owner, then decide whether the architecture defense dossier reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — the mechanism-subtraction council

A final AxiomStore proposal contains a GAT codec, const-generic transaction capacity, dynamic validators, `Any`-based extension metadata, an unsafe inline batch, an enum dispatch layer, a typestate builder, a procedural macro for schema declarations, an async background compactor, and a plugin ABI. The product requirement is only: read two file versions, validate records, apply bounded atomic batches, expose a synchronous library and CLI, and leave room for one future validator integration.

Conduct a mechanism-subtraction council. For every mechanism, name the exact invalid state or extension requirement it removes. Classify its proof cost, compatibility cost, operational cost, and removal path. Reject mechanisms whose benefit is merely stylistic or hypothetical. Your decision must preserve a borrowed read path, bounded mutation, versioned storage, and one open validator boundary.

Produce the smallest architecture that still satisfies the requirement. Then add one unseen change: a caller needs an owned snapshot that can cross threads and survive store replacement. Show which existing boundary changes, which mechanisms remain justified, and which new mechanism—if any—is required. End with a proof ledger mapping each retained mechanism to tests, compile-fail evidence, review, fixtures, or artifact inspection.

## Part 4 — Independent laboratory

Build [Architecture Council](../../labs/module-10-architecture-council/README.md) from its `starter/` package.

Build a compact registry architecture, assign every invariant to one owner, and conduct an architecture council that must reject unnecessary mechanisms as well as approve useful ones.

Before implementation, freeze Architecture Council’s public behavior and the architecture defense dossier. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Complete AxiomStore and the independent AXIOM02 extension. Produce the final defense dossier and show that all earlier guarantees—ownership, errors, memory safety, determinism, boundedness, compatibility, and operability—survive the change.

Update AxiomStore’s architecture defense dossier before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, identify the most sophisticated mechanism in your architecture and argue for deleting it. Compare the simpler replacement on product guarantees, proof burden, compatibility, and maintenance. Keep the mechanism only if the requirement survives that challenge. Record one residual risk that remains visible in the final defense rather than being absorbed into a global claim of correctness.

## Part 6 — Reconstruct and defend

Defend the system in twenty minutes, including five mechanisms deliberately not used and one residual risk that remains after the complete verification portfolio passes.

Finish without notes by reconstructing the architecture defense dossier. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Architecture Council and the AxiomStore increment without seeing your final implementation.
