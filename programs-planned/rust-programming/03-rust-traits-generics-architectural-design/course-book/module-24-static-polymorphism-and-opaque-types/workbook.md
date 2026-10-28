# Workbook — Module 24: Static Polymorphism and Opaque Types

[Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Static Polymorphism and Opaque Types** without relying on surface syntax. Keep the module question in view: *When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Static Polymorphism and Opaque Types** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-method-specific-bound.rs`](../../compiler-labs/module-04/01-method-specific-bound.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-narrow-impl-bound.rs`](../../compiler-labs/module-04/02-narrow-impl-bound.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-independent-impl-trait-arguments.rs`](../../compiler-labs/module-04/03-independent-impl-trait-arguments.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-named-generic-equality.rs`](../../compiler-labs/module-04/04-named-generic-equality.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-opaque-branch-mismatch.rs`](../../compiler-labs/module-04/05-opaque-branch-mismatch.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-opaque-static-dispatch.rs`](../../compiler-labs/module-04/06-opaque-static-dispatch.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-opaque-capability-limit.rs`](../../compiler-labs/module-04/07-opaque-capability-limit.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-generic-type-transition.rs`](../../compiler-labs/module-04/08-generic-type-transition.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

An engine type carries generic parameters for clock, logger, parser, validator, formatter, and ID generator. Only parser and validator vary in production; the rest are fixed utilities.

Reduce generic surface by:

- making fixed collaborators concrete;
- moving helper behavior to free functions;
- keeping method-specific bounds off the whole type;
- using an opaque constructor return only where callers need no concrete name;
- recording which test seams remain and why.

## Part 3 — Focused exercises

1. Derive the minimal bounds for six generic function bodies.
2. Move a method-only bound off a generic struct declaration.
3. Compare two independent `impl Display` arguments with one named `T: Display`.
4. Explain why an opaque return has one hidden concrete type.
5. Repair a conditional opaque return with an enum, then with a trait object; compare costs.
6. Replace a named iterator return type with `impl Iterator` and list lost capabilities.
7. Replace opaque return with an associated GAT when callers need to name the family.
8. Identify three type parameters that should not propagate through an application type.
9. State which static-dispatch performance claims require measurement.
10. Design the generic outer shell of the capstone engine.

### Bound minimization

A static processing pipeline accepts a source, transforms each item, and reports the results. Begin with no bounds and add only those required by each operation. Explain why adding `Clone + Debug + Send + Sync + 'static` “just in case” is not defensive programming but a restriction on valid callers.

Write two APIs: one taking a generic parameter and one taking `impl Trait` in argument position. Show that both describe caller-selected concrete types. Identify the situation in which a named type parameter is necessary because two arguments or the return type must be related.

### Opaque return diagnosis

Repair this design:

```rust
fn choose(flag: bool) -> impl Iterator<Item = u32> {
    if flag {
        0..3
    } else {
        vec![10, 20].into_iter()
    }
}
```

Give three valid repairs—one preserving a single concrete type, one using an enum you own, and one using dynamic dispatch. Compare allocation, API visibility, and extensibility. Do not claim one is universally best.

### RPITIT review

Define a trait method returning `impl Iterator<Item = &str>` from `&self`. Explain what remains opaque to callers, what lifetime relationship is inferred, and why callers cannot require a particular hidden iterator type. Compare this with an associated iterator type and with `Box<dyn Iterator<...>>`.

### Monomorphization claim

Write a precise, limited statement about static dispatch and code generation. Separate the semantic guarantee—calls are type-checked for a concrete implementation—from likely code generation and optimization behavior. Identify what would require measurement rather than assertion.

: static boundary

In Review Engine, choose which boundaries should remain generic and which concrete types should be hidden. Produce a signature map and explain every bound. Remove at least one unnecessary bound from an initial draft.

## Part 4 — Independent laboratory

Build a statically composed validation pipeline whose source code selects concrete validator types.

Requirements:

- a generic `Validate` contract with associated input and error types;
- a pipeline that composes two concrete validators without trait objects;
- minimal bounds at method level;
- an opaque iterator returned from the report view;
- a map operation that consumes the pipeline and changes one strategy type;
- a design memo explaining why runtime heterogeneity is not required.

The executable starter and reference implementation are in [module-04-static-pipeline](../../labs/module-04-static-pipeline/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Define `Engine<S, R>` where `S` is the source and `R` the reporter. Keep both statically dispatched because construction fixes them and reporter output remains useful to the caller.

Do not add the runtime rule registry until Module 25. First prove that one concrete rule set can execute through the generic shell and that source/reporter errors convert at the boundary without forcing `'static` or `Clone` bounds.

## Part 6 — Reconstruct and defend

You must explain static dispatch without performance folklore, distinguish both positions of `impl Trait`, repair an opaque return mismatch with two alternatives, and reduce an overgeneric type.

Oral prompt: **“Which concrete type information does this caller retain, and why is that useful?”**
### Closed-book reconstruction

1. Which concrete type facts survive static dispatch?
2. How do argument-position and return-position `impl Trait` differ in who chooses the type?
3. Why must every return path of one opaque return position resolve to one hidden concrete type?
4. What is the weakest sufficient bound for a function body?
5. When does a large generic surface become architecture noise rather than useful flexibility?

### Independent transfer

Build a statically dispatched transformation pipeline for a different record type. Provide one generic input boundary, one opaque iterator return, and one alternative boxed design. Compare caller knowledge, allocation, code size pressure, diagnostics, and API evolution without claiming performance you did not measure.
