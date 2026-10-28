# Module 92 — Advanced Trait Solving: Goals, Projections, and Type Equality

**92/100** · Course 10 · Module 92 of 100

[Course 10 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [AxiomStore guide](../capstone.md)

## The question

> How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?

## Why this comes now

Course 3 introduced traits as behavioral contracts and associated types as implementation-owned relationships. Mature generic libraries create obligations that are several steps removed from the line that fails: an associated type must implement another trait, two projections must be equal, a blanket implementation may overlap, or an apparently harmless method introduces an unsatisfied well-formedness goal. Module 92 turns error-message reaction into goal-directed reasoning.

Course 3 supplied trait contracts and associated types. Course 5 showed that compiler phases matter. This module deepens both by making each generic error a proof-goal graph rather than a sequence of guessed bounds.

This module turns trait errors from a sequence of compiler appeasement steps into explicit proof search. The key move is to stop reading a diagnostic as one giant sentence. Break it into implementation goals, projection normalization, equality, and well-formedness. Once the graph is visible, the correct boundary for a bound or associated-type equality usually becomes obvious.

## What you will be able to do

After completing this module, you will be able to:

- rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints
- distinguish proving that a trait is implemented from normalizing an associated type selected by that implementation
- choose associated types, generic parameters, and helper traits according to who selects each type relationship
- express equality between associated outputs without forcing unrelated callers to name implementation details
- diagnose ambiguity, unconstrained parameters, recursive obligations, overlap, and missing implied bounds
- design generic pipelines whose error and intermediate types remain precise rather than prematurely erased

## Core model

### The governing model

The governing artifact is a **trait-goal graph**. Nodes are obligations such as `A: Stage`, `<A as Stage>::Output = B::Input`, or `<B as Stage>::Error: Display`. Edges show which operation introduced each obligation. A repair is principled when it supplies the missing evidence at the node’s owner without strengthening unrelated nodes.

### 1. Trait use creates proof goals

A bound such as `T: Iterator` is a request for evidence. Calling `next` also requires the receiver and lifetime relationships to be well formed. Using `T::Item` creates a projection that can only be normalized after an applicable `Iterator` implementation is selected. Read generic code as a sequence of goals: implement, normalize, compare, and prove well formed. This vocabulary makes long diagnostics decomposable.

**Expand the goals.** For a call to `Chain<A, B>::run`, list every implementation and projection goal required before the first statement can type-check.

### 2. Projections are type-level functions selected by implementations

`<S as Stage>::Output` is not a free type variable. It is the output chosen by the `Stage` implementation for `S`. When a pipeline connects two stages, the first output must equal the second input. The equality belongs at the composition boundary. Replacing all associated types with independent generic parameters can make illegal combinations expressible and push the real relationship onto every caller.

**Normalize the projection.** Given `A::Output`, state which implementation must be selected before that name denotes a concrete type. What remains unknown if `A` itself is unconstrained?

### 3. Equality constraints connect local facts

Rust commonly expresses associated-type equality inside a trait bound: `A: Stage<Output = B::Input>`. This tells the solver that normalizing one projection must produce the type required by the next stage. Place the equality where the two components are assembled, not on each component’s standalone definition. That keeps individual stages reusable while making the composition law explicit.

**Place equality locally.** Compare putting `B: Stage<Input = A::Output>` on `Chain` with putting it on `A` or `B` individually. Which design preserves independent reuse?

### 4. Ambiguity is missing selection information

An ambiguous goal is not necessarily a weak compiler. It often means the API leaves more than one legal implementation or conversion path. Fully qualified syntax can identify the intended trait; an input type can carry the missing choice; a local newtype can establish implementation ownership; or the API may need to return a concrete wrapper rather than ask inference to guess. Type annotations are evidence, not decoration.

**Diagnose ambiguity.** Construct two legal conversion paths for the same expression. What additional input, annotation, newtype, or fully qualified path would assign selection authority clearly?

### 5. Recursive goals require a decreasing semantic argument

Recursive trait designs can mirror recursive data, but the solver must still reach a finite proof for each concrete use. Self-referential bounds, blanket implementations that feed themselves, and deeply nested tuples can create overflow or unusable diagnostics. Before adding recursion, identify the measure that decreases: syntax depth, tuple tail, state transition, or wrapper layer. If no measure decreases, the type-level program is not a proof; it is a loop.

**Prove termination.** For a recursive tuple trait, name the type-level measure that decreases. If you cannot name one, replace recursive trait computation with an ordinary data structure.

### 6. Implied bounds are narrower than many readers expect

A type being well formed can imply some lifetime relationships, but Rust does not automatically import every bound used by an implementation into every caller. Public functions must state the obligations they use. If a helper compiles only because its current caller has a stronger bound, extract the helper and see which proof is actually missing. Explicit local bounds improve diagnostics and make refactoring safer.

**Separate implied from required bounds.** Extract a helper method from a strongly bounded impl. Which obligations must now be written on the helper itself?

### 7. Error types reveal architecture

A static pipeline can preserve distinct stage errors through an enum or a generic sum type. Erasing every error into a string makes composition easy only by discarding source, structure, and recovery policy. Decide where error families should remain associated with implementations and where a stable public application error should deliberately erase or translate them. The type solver should support the architecture, not dictate a one-error-fits-all design.

**Preserve error families.** Draw where stage-specific errors remain precise and where AxiomStore deliberately translates them into one public `StoreError`.

### Worked goal decomposition: a borrowed decode pipeline

Suppose a decoder trait chooses both a borrowed view family and an error type, while a validator accepts an owned record:

```rust
trait Decode {
    type View<'a> where Self: 'a;
    type Error;
    fn decode<'a>(&self, bytes: &'a [u8]) -> Result<Self::View<'a>, Self::Error>;
}

trait OwnsRecord {
    type Owned;
    fn own(self) -> Self::Owned;
}
```

A helper that decodes and then owns a value needs more than `D: Decode`. It needs a goal for every borrow used by the call: `D::View<'a>: OwnsRecord`, and it needs the owned projection to equal the application’s record type. Write those as separate obligations rather than hiding them in an enormous trait alias. The lifetime-indexed projection is selected only after `D` is known; the owned projection is selected only after the view type is normalized.

Now ask where each equality belongs. Requiring every decoder view to own into AxiomStore’s `Record` would make a reusable codec depend on one application model. Requiring the equality on the helper or adapter that connects the codec to AxiomStore preserves independent codec reuse. Conversely, making `Owned` another freely chosen generic parameter would allow callers to claim a conversion target that the view never provides.

This decomposition also improves errors. A failure to select `D: Decode` is different from a view that lacks `OwnsRecord`, which is different again from an owned type that does not equal `Record`. The signature should let the diagnostic point to that exact edge. When a single helper produces a page of obligations, draw the graph and consider splitting the helper at a stable intermediate boundary instead of adding aliases that hide the same complexity.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Who chooses a related type? | associated type when the implementation owns one relationship | independent generic parameters that permit nonsense combinations |
| Where should equality be required? | the composition site connecting two components | every standalone component definition |
| Why is selection ambiguous? | missing input evidence, competing impls, or unconstrained parameter | random annotations without a goal graph |
| Should errors be erased? | the boundary that owns stable recovery policy | the first generic helper that finds multiple error types inconvenient |

### A rigorous working procedure

1. Copy the failing signature and replace every shorthand projection with fully qualified form.
2. List the goals introduced by each operation in body order. Distinguish implementation selection, projection normalization, equality, and well-formedness.
3. Mark which component owns each type choice: caller, trait implementation, composition boundary, or application boundary.
4. Remove all speculative bounds. Add back only the obligation actually used at the narrowest owning boundary.
5. Build one invalid composition that should fail at assembly time and one valid composition with distinct error types.
6. Translate errors only where stable recovery policy begins; do not erase them inside reusable stages.

### Failure patterns and principled repairs

Trait-system failures become tractable when each obligation is written as a separate goal and each associated type is treated as a projection that must normalize under known assumptions. The principled repair adds the missing relationship at the boundary that owns it; it does not scatter concrete type annotations until inference happens to stop complaining.

### Adding bounds until the error disappears

Reduce the diagnostic to one unsatisfied goal and add only the evidence used by that function body.

### Coupling independent components globally

Move associated-type equality to `Chain<A, B>` or the constructor that assembles them.

### Using strings to avoid generic error design

Preserve typed stage errors, then translate once at the application boundary.

### Creating recursive obligations without a decreasing measure

Identify the smaller type-level input or replace recursive trait computation with runtime data.

### What the compiler cannot decide for you

The trait solver can establish that a set of goals follows from the visible implementations and bounds. It cannot decide whether an associated type or generic parameter expresses the right extension authority, whether a blanket implementation is a responsible public commitment, or whether preserving a large error type is worth the API cost. Those are architecture and evolution decisions.

Treat compiler ambiguity as information: the program has not assigned enough authority to select one legal relationship. The repair should clarify ownership of the choice, not merely overwhelm inference with annotations.

## Use the idea in a complete program

Before compiling `Chain`, write the complete goal graph. Pay special attention to the moment when `A::Output` is equated with `B::Input`; that equality is the reason the second call is legal, not an incidental compiler inference.

```rust
trait Stage {
    type Input;
    type Output;
    type Error;

    fn run(&self, input: Self::Input) -> Result<Self::Output, Self::Error>;
}

struct Chain<A, B>(A, B);

enum ChainError<EA, EB> {
    First(EA),
    Second(EB),
}

impl<A, B> Stage for Chain<A, B>
where
    A: Stage,
    B: Stage<Input = A::Output>,
{
    type Input = A::Input;
    type Output = B::Output;
    type Error = ChainError<A::Error, B::Error>;

    fn run(&self, input: Self::Input) -> Result<Self::Output, Self::Error> {
        let middle = self.0.run(input).map_err(ChainError::First)?;
        self.1.run(middle).map_err(ChainError::Second)
    }
}
```

### Trace the example

Start from `impl<A, B> Stage for Chain<A, B>`. Expand `A: Stage` and `B: Stage<Input = A::Output>` into named goals. For `run`, trace the input type through the first projection, the `middle` binding, the second input equality, and the final output projection. Then trace each `map_err` into the two variants of `ChainError`.

Delete only the associated-type equality and record the earliest failing expression. Next, redesign the pipeline with three independent generic type parameters and show the nonsensical combinations the new API admits. The exercise is complete when you can explain why the more permissive signature is weaker, not merely longer.

### Use it in AxiomStore

AxiomStore separates decoding, schema validation, and encoding through precise associated families. The codec chooses its borrowed view type and decode error. Validators accept one owned record type. Composition requires explicit projection equality, and translation into the stable store error occurs only at the public boundary. You will build the goal graph before writing bounds so the signatures explain the relationship rather than accumulate compiler appeasement.

AxiomStore’s codec boundary needs a projection record:

```text
component
implementation goal
associated family
normalization trigger
equality required at composition
error family before translation
public translation boundary
```

Use it for decoding, borrowed views, and validation. The codec owns its view family; the runtime validator registry does not. Keep that distinction visible so Course 95 can erase validators without erasing the lifetime relationship of decoded views.

## Practice sequence

1. **Manual normalization.** Evaluate a nested pair of associated types to a concrete type and show every implementation selection used.
2. **Unconstrained parameter repair.** Produce three repairs—input evidence, associated type, and explicit constructor—and compare who chooses the missing type.
3. **Typed error composition.** Extend `ChainError` to three stages without converting any error to text. State where an application may later translate it.
4. **Overlap analysis.** Design two blanket impls that overlap for one concrete type. Explain the coherence conflict and repair ownership with a local newtype or narrower domain.
5. **Goal minimization.** Take a function with five bounds and prove which two are actually used by the body.

Then complete the [workbook](workbook.md) and [Projection-Driven Pipeline](../../labs/module-02-projection-driven-pipeline/README.md). Each compiler investigation must be annotated with the smallest unsatisfied goal, not just the final diagnostic paragraph.

## Ready to continue

You are ready for lifetime-indexed type families when you can normalize projections by hand, place equality at the composition boundary, distinguish ambiguity from missing implementation, and preserve distinct stage errors until a deliberate translation point. You should be able to delete an unnecessary bound and explain why the program remains well formed.

## Primary Rust references

- The Rust Reference: trait bounds and associated items
- The rustc development guide: trait solving and canonical goals
- The standard library documentation for Iterator and TryFrom as associated-type examples

When consulting trait-solver material, separate stable language behavior from rustc’s current internal terminology. Use the internal model to understand goals; use the Reference and public API behavior for lasting contracts.

## Continue

1. Complete the [workbook](workbook.md) without consulting answers.
2. Build [Projection-Driven Pipeline](../../labs/module-02-projection-driven-pipeline/README.md).
3. Apply Module 92 in the [AxiomStore engineering guide](../capstone.md).
4. Review the [solutions](solutions.md) only after preserving your own predictions and design record.
