# Reasoned Solutions — Module 91: Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-01-compiler-evidence-notebook/README.md) · [AxiomStore guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 91: Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**. Compare the reasoning against this question: *When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction

### Prediction 1 — Method resolution before MIR

Name resolution and type checking select the inherent method available through `&self`; MIR is downstream evidence. Fully qualified trait syntax would assign different authority explicitly.

### Prediction 2 — Loan ends before lexical block

The borrow can end at its last use under non-lexical lifetime analysis. The later push is legal only when no returned reference remains live.

### Prediction 3 — Partial move and drop

Without an outer `Drop`, initialized unmoved fields are destroyed. A type implementing `Drop` generally cannot have fields moved out through ordinary pattern matching because the destructor expects the whole value.

### Prediction 4 — Artifact claim

The observation describes one pinned artifact; it does not establish a language guarantee or universal generic sharing. Record toolchain, target, profile, features, LTO, codegen units, and inspected symbol evidence.

## Part 2 — Diagnose and repair

Judge every repair against the source-to-artifact evidence ladder: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Clone inserted after borrow error

**Causal defect.** A parser clones its whole input buffer because a returned slice blocks later cursor mutation. Repair the place or lifetime relationship while preserving borrowed output.

**Principled repair.** Shorten the returned borrow, split cursor state from backing storage, or change sequencing. Cloning abandons the intended borrowing contract.

The negative case should reintroduce **Clone inserted after borrow error** while preserving the surrounding requirement. The source-to-artifact evidence ladder must identify the first phase at which the original assumption becomes invalid.

### Repair 2 — Runtime experiment used as drop proof

**Causal defect.** A test prints destructor order and the documentation treats that exact output as the language contract.

**Principled repair.** Derive required destruction from initialization and exit edges. Keep print order as one observation and remove claims that optimization or future toolchains cannot preserve.

The negative case should reintroduce **Runtime experiment used as drop proof** while preserving the surrounding requirement. The source-to-artifact evidence ladder must identify the first phase at which the original assumption becomes invalid.

### Repair 3 — Assembly used to explain a method error

**Causal defect.** A review begins with assembly to explain why `item.render()` selects the wrong method.

**Principled repair.** Return to resolution: enumerate inherent and trait candidates, autoderef/autoref, and bounds. Machine code exists only after selection succeeds.

The negative case should reintroduce **Assembly used to explain a method error** while preserving the surrounding requirement. The source-to-artifact evidence ladder must identify the first phase at which the original assumption becomes invalid.

## Part 3 — Focused exercises

### Exercise 1 — Receiver adjustment table

The construction should answer: Create three types with overlapping inherent and trait methods. For each call, record candidate, adjustment, and fully qualified alternative.

The decisive acceptance criterion is: The table predicts every call and does not appeal to source proximity.

For **Receiver adjustment table**, apply the source-to-artifact evidence ladder to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 2 — Control-flow drop graph

The construction should answer: Write a function with `?`, a `match`, partial initialization, and an observable destructor. Draw cleanup on normal and error paths.

The decisive acceptance criterion is: Every live value appears exactly once on each applicable exit.

For **Control-flow drop graph**, apply the source-to-artifact evidence ladder to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 3 — Place projection repair

The construction should answer: Diagnose a conflict involving two fields and an indexed element. Produce one API repair that exposes disjointness.

The decisive acceptance criterion is: The repair changes places or borrow duration; no blanket cloning is accepted.

For **Place projection repair**, apply the source-to-artifact evidence ladder to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 4 — Scoped artifact note

The construction should answer: Inspect one generic and one dynamic path in a fixed release build.

The decisive acceptance criterion is: The note includes semantic parity, build identity, observation, and an explicit expiry condition.

For **Scoped artifact note**, apply the source-to-artifact evidence ladder to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Cross-course transfer

Full credit may conclude that **Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.

### Applied case study — one error, four representations

The first notebook entry classifies the failed collection as a trait-solving obligation. The source asks the compiler to prove that the target collection can be built from the iterator's projected item type. HIR preserves enough typed structure to locate the call and projection; the trait solver decides whether the goal is satisfiable. MIR may show the elaborated control flow after type checking, but it is not the phase that invents the missing `FromIterator` relationship.

The second entry treats record ordering as a product invariant. Once the program type-checks, neither HIR nor MIR proves that the chosen traversal order matches the specification. A behavioral oracle with intentionally permuted input is the relevant evidence. The smallest repair is to make ordering authority explicit—perhaps by sorting at one named boundary or by selecting an ordered source—not to reinterpret a compiler dump as a semantic test.

The third entry records the two large symbols as artifact observations. They are useful only with the exact compiler, target, profile, feature set, and source revision. They can motivate a dispatch experiment, but they cannot prove that dynamic dispatch is preferable or that the generic implementation is incorrect.

A disciplined sequence is therefore: isolate the trait goal; read the ordinary diagnostic; inspect typed or MIR representations only for unresolved compiler behavior; establish runtime parity; then compare release artifacts. The trait diagnostic cannot choose product ordering, the runtime test cannot explain a type error, and symbol inspection cannot establish portability or correctness.

## Part 4 — Independent laboratory

A complete [Compiler Evidence Notebook](../../labs/module-01-compiler-evidence-notebook/README.md) satisfies its public contract and makes the source-to-artifact evidence ladder inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build an evidence notebook that classifies claims by phase, records what remains unknown, and includes one drop experiment whose runtime observation is kept separate from the semantic argument.

The transfer variant for Compiler Evidence Notebook must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

A complete transfer answer draws two different graphs. The first begins with the snapshot-owned byte vector, follows slices through codec decoding, and ends when the cursor borrow releases the `RecordView`. The second begins with an owned candidate map and follows every pre-install failure back to the unchanged archive. For each edge, identify whether the compiler, runtime validation, operating system, or artifact inspection supplies the evidence; do not promote a symbol or assembly observation into a language contract.

A strong capstone change keeps the responsibility described by the source-to-artifact evidence ladder local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Explain a borrow rejection, a destructor obligation, and a code-size observation using three different evidence layers. Then justify why the compiler cannot select the product redesign after the borrow rejection.

The defense passes when it reconstructs the source-to-artifact evidence ladder from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.

## Deep reasoning and transfer

### Decisive model

> When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?

Build a **compiler-phase record**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Translate source constructs into a control-flow and place-oriented model suitable for borrow, move, and drop reasoning.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Identify when an observation is a language guarantee, a compiler implementation detail, or generated machine-code evidence.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Use compiler diagnostics, expanded code, MIR-oriented reasoning, and assembly inspection without treating any single view as the complete semantics.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Explain non-lexical lifetimes, temporary scopes, partial moves, and destructor placement through explicit control-flow points.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the compiler-phase record.

### Reference implementation comparison

For [Compiler Evidence Notebook](../../labs/module-01-compiler-evidence-notebook/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In AxiomStore, Module 91 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**, which relationship decides this question: “When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to AxiomStore?
