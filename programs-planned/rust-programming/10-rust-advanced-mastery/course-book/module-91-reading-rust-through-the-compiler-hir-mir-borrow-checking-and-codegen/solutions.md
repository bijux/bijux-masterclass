# Module 91 Solutions — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

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

A strong answer updates the source-to-artifact evidence ladder and includes a negative case that fails for the original cause.

### Repair 2 — Runtime experiment used as drop proof

**Causal defect.** A test prints destructor order and the documentation treats that exact output as the language contract.

**Principled repair.** Derive required destruction from initialization and exit edges. Keep print order as one observation and remove claims that optimization or future toolchains cannot preserve.

A strong answer updates the source-to-artifact evidence ladder and includes a negative case that fails for the original cause.

### Repair 3 — Assembly used to explain a method error

**Causal defect.** A review begins with assembly to explain why `item.render()` selects the wrong method.

**Principled repair.** Return to resolution: enumerate inherent and trait candidates, autoderef/autoref, and bounds. Machine code exists only after selection succeeds.

A strong answer updates the source-to-artifact evidence ladder and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Receiver adjustment table

The construction should answer: Create three types with overlapping inherent and trait methods. For each call, record candidate, adjustment, and fully qualified alternative.

The decisive acceptance criterion is: The table predicts every call and does not appeal to source proximity.

Evaluate the result through the source-to-artifact evidence ladder; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Control-flow drop graph

The construction should answer: Write a function with `?`, a `match`, partial initialization, and an observable destructor. Draw cleanup on normal and error paths.

The decisive acceptance criterion is: Every live value appears exactly once on each applicable exit.

Evaluate the result through the source-to-artifact evidence ladder; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Place projection repair

The construction should answer: Diagnose a conflict involving two fields and an indexed element. Produce one API repair that exposes disjointness.

The decisive acceptance criterion is: The repair changes places or borrow duration; no blanket cloning is accepted.

Evaluate the result through the source-to-artifact evidence ladder; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Scoped artifact note

The construction should answer: Inspect one generic and one dynamic path in a fixed release build.

The decisive acceptance criterion is: The note includes semantic parity, build identity, observation, and an explicit expiry condition.

Evaluate the result through the source-to-artifact evidence ladder; helper names may differ, but the invariant owner and adversarial case must be explicit.

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
