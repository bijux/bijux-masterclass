# Workbook — Module 22: Associated Types and Type Families

[Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Associated Types and Type Families** without relying on surface syntax. Keep the module question in view: *When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Associated Types and Type Families** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-associated-projection.rs`](../../compiler-labs/module-02/01-associated-projection.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-ambiguous-associated-type.rs`](../../compiler-labs/module-02/02-ambiguous-associated-type.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-generic-relationship-multiplicity.rs`](../../compiler-labs/module-02/03-generic-relationship-multiplicity.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-associated-type-uniqueness.rs`](../../compiler-labs/module-02/04-associated-type-uniqueness.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-generic-associated-type.rs`](../../compiler-labs/module-02/05-generic-associated-type.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-lending-borrow-overlap.rs`](../../compiler-labs/module-02/06-lending-borrow-overlap.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-unspecified-associated-type.rs`](../../compiler-labs/module-02/07-unspecified-associated-type.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-gat-dyn-incompatibility.rs`](../../compiler-labs/module-02/08-gat-dyn-incompatibility.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A `Codec<T, E, C>` trait has three generic parameters, every implementation supports only one output and error type, and callers carry five type arguments through the entire program.

Refactor by:

- identifying which relationships are canonical per codec;
- moving those to associated types;
- leaving caller-selected configuration generic only if multiple relationships are real;
- adding equality constraints only where exact identity matters;
- producing a separate erased adapter if runtime heterogeneity is required.

Your final memo must show one design where generic parameters are preferable and one where associated types are preferable.

## Part 3 — Focused exercises

1. Classify ten relationships as generic parameter, associated type, GAT, or ordinary value.
2. Redesign `Parser<Output, Error>` when each parser has one output and one error family.
3. Show a type that legitimately implements `Convert<String>` and `Convert<Vec<u8>>`.
4. Write a `Source` consumer with the weakest sufficient bound on `Source::Item`.
5. Replace an exact associated-type equality with a capability bound and explain the newly accepted callers.
6. Design an associated constant for a wire-format magic number; explain why run-time chunk size is not one.
7. Implement a minimal lending row trait and prove that two returned rows cannot coexist across mutation.
8. Split a GAT-heavy API into a low-level borrowed layer and an owned adapter.
9. Make a trait object type with fixed associated `Item` and `Error` types.
10. Explain why a GAT-bearing trait cannot be the capstone's dynamic rule interface.

### Who chooses the type?

Design a parsing interface for three formats. Each parser has one natural output type and one natural error type. Compare these signatures:

```rust
trait Parser<T, E> {
    fn parse(&self, input: &str) -> Result<T, E>;
}

trait Parser {
    type Output;
    type Error;
    fn parse(&self, input: &str) -> Result<Self::Output, Self::Error>;
}
```

For each form, state who selects `Output` and `Error`, whether one parser type may support several outputs, and what ambiguity appears at call sites. Choose one for the product and defend it.

### Projection exercise

Given `P: Parser`, write a function that accepts two parsers only when they produce the same output type but may have different errors. Then write a second function that accepts a parser whose output is exactly `Record`. Explain the equality constraints in prose before writing syntax.

### Associated constant or method?

A storage codec has a version tag, a maximum record length, and a default delimiter. Decide which belong as associated constants, instance methods, or constructor configuration. Test your answer against two implementations that share a type but require different runtime delimiters.

### Borrowed families

Design a cursor trait that yields views borrowing from `self`. First try a plain associated type and write down why `type Item = &str` cannot express a lifetime chosen by each borrow of the cursor. Then sketch a generic associated type:

```rust
trait Cursor {
    type Item<'a>
    where
        Self: 'a;

    fn current<'a>(&'a self) -> Option<Self::Item<'a>>;
}
```

State what the `where Self: 'a` relationship says. Do not add a GAT when an ordinary iterator yielding owned values would satisfy the product.

: family map

For the Review Engine, draw a table for `Source`, `Rule`, and `Reporter`: which related types are chosen by the implementation, which are selected per method call, and which should remain concrete domain types. Identify one relationship that would become weaker if converted into an unconstrained generic parameter.

## Part 4 — Independent laboratory

Implement a tabular source abstraction with two layers:

- `LendingRows`, whose `Row<'a>` borrows from the source's current buffer;
- `OwnedRows`, an adapter that materializes durable `OwnedRow` values.

The lab must demonstrate why ordinary `Iterator` cannot express the lending relationship and must include a compile-fail example preventing a borrowed row from surviving the next mutable advance.

The solution must not expose the GAT to callers that only need owned rows.

The executable starter and reference implementation are in [module-02-associated-families](../../labs/module-02-associated-families/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Define:

```rust
trait Source {
    type Item;
    type Error;
    fn load(self) -> Result<Vec<Self::Item>, Self::Error>;
}

trait Reporter {
    type Output;
    type Error;
    fn report(&self, review: &Review) -> Result<Self::Output, Self::Error>;
}
```

The capstone fixes `Source::Item = Submission` at the engine boundary but preserves implementation-specific errors until they are converted into `EngineError`. Do not erase source and reporter types. Their selection occurs at construction, and callers benefit from concrete output types.

## Part 6 — Reconstruct and defend

Pass only when you can derive the associated-item design from relationship cardinality, implement and explain one GAT, state why it constrains caller control flow, and show how associated items affect trait-object formation.

Oral prompt: **“Why is an associated type not merely a generic parameter written elsewhere?”**
### Closed-book reconstruction

1. Who selects a generic parameter, and who selects an associated type?
2. What relationship cardinality makes an associated type the clearer model?
3. What does a projection such as `S::Item` mean at a use site?
4. When does a GAT express a family of borrowed outputs rather than one fixed type?
5. How can associated items affect dyn compatibility?

### Independent transfer

Design a parser family whose view type borrows from each input invocation. Compare a GAT-based trait with a trait that returns an owned value and with an ordinary generic function. State who chooses every type, how long each result may live, and which caller control-flow constraints each design imposes.
