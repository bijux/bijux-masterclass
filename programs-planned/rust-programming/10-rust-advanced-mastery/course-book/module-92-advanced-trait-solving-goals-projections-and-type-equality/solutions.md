# Module 92 Solutions — Advanced Trait Solving: Goals, Projections, and Type Equality

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Pipeline composition

The solver needs both implementations, normalized projections, and equality between the middle types. The second stage call fails because `middle` cannot be proven to have `B::Input`.

### Prediction 2 — Ambiguous conversion

The goal is ambiguous. A return annotation, fully qualified conversion, or a constructor/newtype that owns the target choice can resolve it; random unrelated bounds cannot.

### Prediction 3 — Implied bound myth

The helper must state the obligations its body uses. Bounds on a former caller are not automatically imported into an independent item.

### Prediction 4 — Recursive trait goal

The obligation can recurse or overflow. Identify a decreasing measure or move the recursion into runtime data.

## Part 2 — Diagnose and repair

Judge every repair against the trait-goal graph: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Global equality constraint

**Causal defect.** Two independently useful stages are defined with a global equality that couples all implementations.

**Principled repair.** Move the equality to the `Chain` impl or constructor where the components meet. Standalone stages keep their own associated families.

A strong answer updates the trait-goal graph and includes a negative case that fails for the original cause.

### Repair 2 — String-erased stage errors

**Causal defect.** A reusable pipeline converts every stage error to `String` to make composition easy.

**Principled repair.** Preserve a typed sum such as `ChainError<A::Error, B::Error>` and translate once at the application boundary that owns recovery policy.

A strong answer updates the trait-goal graph and includes a negative case that fails for the original cause.

### Repair 3 — Bound accumulation

**Causal defect.** A generic helper has ten bounds added one by one until it compiles.

**Principled repair.** Remove all bounds, inspect each operation, and restore only the goals actually introduced by the body. Split the helper if one signature is carrying unrelated proof domains.

A strong answer updates the trait-goal graph and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Goal expansion

The construction should answer: Expand a nested `Iterator<Item = Result<T, E>>` consumer into implementation, projection, equality, and well-formedness goals.

The decisive acceptance criterion is: Every operation is connected to the goal that authorizes it.

Evaluate the result through the trait-goal graph; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Three-stage error family

The construction should answer: Compose parse, validate, and encode stages without text erasure.

The decisive acceptance criterion is: The final error identifies the failing stage and retains its source type.

Evaluate the result through the trait-goal graph; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Ambiguity redesign

The construction should answer: Produce three APIs that resolve one ambiguous target by caller input, implementation ownership, and explicit constructor.

The decisive acceptance criterion is: The comparison names who chooses the type in each design.

Evaluate the result through the trait-goal graph; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Coherence boundary

The construction should answer: Create an overlapping blanket-impl proposal and repair it with a local newtype or narrower trait domain.

The decisive acceptance criterion is: The final implementation ownership is legal and architecturally justified.

Evaluate the result through the trait-goal graph; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **Advanced Trait Solving: Goals, Projections, and Type Equality** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — projected errors in a storage pipeline

The pipeline needs three capability goals and two local normalization goals. The decoder must implement `Decode`; the validator must implement `Validate`; the materializer must implement `Materialize`. At the assembly boundary, the decoder's lending view for the current borrow must equal the validator's accepted input family, and the validator's accepted output must equal the materializer's input. Those equalities are properties of this composition, not universal laws of every decoder or validator, so placing them on the base traits would reject otherwise reusable implementations.

Error identity remains associated with each stage. The outer adapter can define `PipelineError<D::Error, V::Error, M::Error>` and map failures into the corresponding variant. Replacing every error with `String` destroys which stage failed, prevents typed recovery, and imposes allocation without solving a type relationship.

Ambiguity appears when code refers to `T::Item` but more than one trait in scope defines `Item`, or when the implementor cannot be inferred from surrounding arguments. The repair is a fully qualified projection such as `<D as Decode>::View<'a>`, not an unrelated type annotation elsewhere.

A causal negative case pairs a decoder returning `Utf8Record<'a>` with a validator whose input family is `BinaryRecord<'a>`. Both satisfy their own traits, but the composition goal cannot normalize the two projections to the same type. The expected compiler evidence is an associated-type mismatch at the chain implementation or constructor. Adding a conversion stage is principled; erasing both views into owned strings merely deletes the zero-copy contract.

## Part 4 — Independent laboratory

A complete [Projection-Driven Pipeline](../../labs/module-02-projection-driven-pipeline/README.md) satisfies its public contract and makes the trait-goal graph inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a three-stage pipeline whose associated input, output, and error families connect only at the assembly boundary. Mismatched composition must be rejected before execution.

The transfer variant for Projection-Driven Pipeline must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Write the goal graph for AxiomStore’s codec, borrowed view, owned record conversion, and validator boundary. Keep codec errors precise until translation into `StoreError`; do not make runtime validators generic over the codec’s lending family.

A strong capstone change keeps the responsibility described by the trait-goal graph local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Normalize one nested projection aloud, identify the owner of every type choice, and explain why a more generic signature can admit nonsense rather than improve reuse.

The defense passes when it reconstructs the trait-goal graph from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
