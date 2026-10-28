# Module 24 — Static Polymorphism and Opaque Types

**Course 3 · Day 4 · Module 24 of 100**
`██████░░░░░░░░░░░░░░░░░░░` **24/100**

[Program](../../../README.md) · [Course 3](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-static-pipeline/README.md) · [Review Engine guide](../capstone.md)

[← Module 23: Coherence and Implementation Ownership](../module-23-coherence-and-implementation-ownership/index.md) · [Module 25: Trait Objects and Dynamic Polymorphism →](../module-25-trait-objects-and-dynamic-polymorphism/index.md)

## The question

> When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

## Why this comes now

With legal implementations in place, static polymorphism can be designed deliberately. Generic parameters, precise bounds, monomorphization, and opaque return types are studied as one family: the concrete type remains known to the compiler even when an API chooses not to name it publicly.

### Prerequisite bridge

Module 23 established **Coherence and Implementation Ownership**. Before continuing, verify that you can produce an implementation-ownership map for a public api. This module preserves that capability and adds the ability to design generic functions and types with the weakest sufficient bounds. Module 25, **Trait Objects and Dynamic Polymorphism**, will rely on both when it asks: *When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?*

### Scope boundary

This module owns the reasoning for **static polymorphism and opaque types** inside Course 3. The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Design generic functions and types with the weakest sufficient bounds.
- Distinguish argument-position and return-position `impl Trait`.
- Explain monomorphization without promising optimization outcomes.
- Choose static dispatch when concrete type identity carries useful guarantees.
- Control generic API complexity through boundary placement.

## Core model

### Static polymorphism keeps the concrete type in the type system

A generic function is checked once against its bounds and instantiated for the concrete types used by the program:

```rust
pub trait Rule {
    fn accepts(&self, input: &str) -> bool;
}

pub fn accepted_count<R>(rule: &R, inputs: &[String]) -> usize
where
    R: Rule,
{
    inputs.iter().filter(|input| rule.accepts(input)).count()
}
```

The caller chooses `R`. Inside the function, Rust knows that `R` is one concrete type satisfying `Rule`. This permits static method resolution and optimization based on that type. It also means a `Vec<R>` is homogeneous: all elements have the same concrete `R`.

Do not translate “static dispatch” into “always faster.” Monomorphization can enable inlining and remove indirection, but it may increase compile time and code size, and performance depends on the workload and optimizer. The reliable claim is about type information and dispatch choice, not speed.

### Bounds should expose only what the implementation needs

Start from the body:

```rust
fn first_label<T>(items: &[T]) -> Option<String>
where
    T: Label,
{
    items.first().map(Label::label)
}
```

If the body does not clone, compare, hash, or debug `T`, those bounds do not belong. Over-bounding has several costs:

- valid caller types are rejected;
- future implementation changes may become breaking because callers relied on the broader contract;
- the signature misrepresents what the algorithm needs;
- test doubles require irrelevant behavior.

Sometimes a stronger bound is a deliberate product requirement—for example, a returned task may need `Send + 'static` because another thread owns it. State that reason. Do not add bounds in anticipation of hypothetical implementation choices.

### `T: Trait` and argument-position `impl Trait`

These two functions accept one value implementing `Display`:

```rust
fn show_generic<T: std::fmt::Display>(value: T) -> String {
    value.to_string()
}

fn show_opaque(value: impl std::fmt::Display) -> String {
    value.to_string()
}
```

For one parameter, they are often interchangeable to callers. A named type parameter becomes necessary when the relationship appears more than once:

```rust
fn same_type<T: Display>(left: T, right: T) -> String {
    format!("{left} | {right}")
}
```

By contrast:

```rust
fn possibly_different(left: impl Display, right: impl Display) -> String {
    format!("{left} | {right}")
}
```

Each `impl Display` in argument position introduces its own anonymous type parameter, so the arguments may have different concrete types.

Use named parameters when callers or the body need relationships among arguments, associated types, or return types. Use argument-position `impl Trait` when the relationship is local and the shorter signature is clearer.

### Return-position `impl Trait` hides one concrete type

A function returning `impl Iterator<Item = u32>` chooses one concrete iterator type but does not expose its name:

```rust
fn even_values(input: &[u32]) -> impl Iterator<Item = u32> + '_ {
    input.iter().copied().filter(|n| n % 2 == 0)
}
```

The caller knows the returned value implements the stated bounds. The function body must return one concrete type on every path:

```rust,compile_fail
fn values(flag: bool) -> impl Iterator<Item = u32> {
    if flag {
        0..3
    } else {
        vec![1, 2, 3].into_iter()
    }
}
```

Both branches implement `Iterator<Item = u32>`, but they are different concrete iterator types. `impl Trait` is not a trait object and does not create runtime heterogeneity.

Repairs include:

- return an enum that wraps the finite alternatives;
- restructure the pipeline so both branches have one type;
- return `Box<dyn Iterator<Item = u32>>` when runtime erasure is justified;
- collect into one owned collection if eagerness is acceptable.

Each repair changes ownership, allocation, dispatch, or laziness. Choose from the product requirement.

### Hidden types still carry lifetimes

The returned iterator above borrows `input`, so `+ '_` makes the relationship visible. Opaque return types hide the concrete type, not its obligations. The value cannot outlive the source slice.

A closure-returning function has the same property:

```rust
fn prefixed<'a>(prefix: &'a str) -> impl Fn(&str) -> String + 'a {
    move |value| format!("{prefix}{value}")
}
```

The closure owns a reference with lifetime `'a`; the opaque type therefore carries `'a`.

### Return-position `impl Trait` in traits

A trait method can return an opaque type associated with each implementation:

```rust
trait Names {
    fn names(&self) -> impl Iterator<Item = &str>;
}
```

This can make static APIs concise. It also has consequences:

- each implementation chooses its own hidden concrete return type;
- callers use the stated bounds, not the hidden type;
- methods returning opaque types are not dispatchable through ordinary trait objects;
- public bounds on the opaque result are part of the contract.

If dynamic dispatch is a goal, a boxed iterator, a callback-based method, an associated iterator type, or a separate dyn-facing trait may be more appropriate. Do not force one trait to satisfy incompatible static and dynamic consumers.

### Generic type parameters move complexity

A generic struct stores one concrete strategy in its type:

```rust
struct Engine<R> {
    rule: R,
}

impl<R: Rule> Engine<R> {
    fn evaluate(&self, input: &str) -> bool {
        self.rule.accepts(input)
    }
}
```

This gives static dispatch and no trait-object allocation. It also makes the strategy part of `Engine`'s type, which can propagate through APIs and prevent a homogeneous collection of engines with different `R` values.

That propagation is not inherently bad. It is appropriate when the strategy is fixed for the value’s lifetime and known to the caller. It becomes friction when runtime reconfiguration or heterogeneous storage is central.

### Choose static dispatch from the variation schedule

Static polymorphism is a strong default when:

- the concrete implementation is chosen while compiling the caller;
- one value uses one strategy type;
- heterogeneous storage is unnecessary;
- associated types and generic methods are important;
- the API benefits from exposing compile-time relationships.

Prefer an enum when the implementation set is closed and pattern matching is useful. Prefer a trait object when implementations are open or selected at runtime and a dyn-compatible erased surface is sufficient. Prefer an ordinary function or closure when only one operation varies.

The question is not “generics or trait objects?” in isolation. It is **when is variation selected, who owns the set of alternatives, and what type information must remain available afterward?**

#### The concrete type is known after instantiation

```rust
fn evaluate<R: Rule>(rule: &R, submission: &Submission) -> Vec<Finding> {
    let mut out = Vec::new();
    rule.evaluate(submission, &mut out);
    out
}
```

The source function is generic, but each call uses a concrete `R`. Rust type-checks the body against the trait contract, then code generation may monomorphize used instantiations.

#### What static dispatch does and does not promise

It preserves concrete type information and avoids trait-object dispatch semantics. It does **not** guarantee inlining, zero allocation, smaller binaries, or faster execution. Those are implementation and workload questions for Course 9.

#### Architectural effects

- callers often carry the concrete type in their own signatures;
- heterogeneous collections are difficult without an enum or erasure;
- associated types remain available precisely;
- methods not dyn-compatible can still be used;
- compiler diagnostics can expose long concrete type compositions.

Use static polymorphism because the selection time and guarantees fit, not because “generics are always faster.”

#### Let the body justify every requirement

```rust
fn join_labels<I>(items: I) -> String
where
    I: IntoIterator,
    I::Item: AsRef<str>,
{
    items.into_iter()
        .map(|item| item.as_ref().to_owned())
        .collect::<Vec<_>>()
        .join(",")
}
```

The function accepts many containers and string-like item types. But flexibility has cost: more generic surfaces, more diagnostics, and more implementation combinations to test.

#### Minimal does not mean maximally abstract

A concrete `&[String]` parameter may be clearer if every caller already owns a slice of strings. The weakest sufficient *bound* is relevant after a generic boundary is justified. Do not generalize a function merely because it is possible.

#### Bounds at the narrowest location

A generic type may support methods with different requirements:

```rust
struct Pair<T>(T, T);

impl<T> Pair<T> {
    fn first(&self) -> &T { &self.0 }
}

impl<T: PartialOrd> Pair<T> {
    fn max(&self) -> &T {
        if self.0 >= self.1 { &self.0 } else { &self.1 }
    }
}
```

Placing `T: PartialOrd` on the entire struct would prevent storing non-orderable pairs even when only `first` is used.

#### A type parameter becomes part of representation

```rust
struct Pipeline<S, V> {
    source: S,
    validator: V,
}
```

Every `Pipeline<FileSource, StrictValidator>` has a distinct concrete type from `Pipeline<MemorySource, LenientValidator>`. This can encode configuration at compile time, but it can also spread complex type names through the application.

#### Keep generic complexity at boundaries

Use constructor functions and type aliases to improve local readability, but do not hide semantically important differences. A public alias can itself become an API promise.

#### Generic methods can vary independently

```rust
impl<S, V> Pipeline<S, V> {
    fn map_validator<W>(self, validator: W) -> Pipeline<S, W> {
        Pipeline { source: self.source, validator }
    }
}
```

The method consumes the pipeline and changes its concrete type. This is useful for builder-like composition and typestate, which Module 27 develops.

#### Type-parameter proliferation

When a type acquires six strategy parameters, ask whether all variations are selected at the same time and needed in every method. Some belong behind concrete adapters; some may be dynamic; some may not be true variation.

#### Anonymous generic parameter

```rust
fn print_label(value: &impl std::fmt::Display) {
    println!("{value}");
}
```

For ordinary use, argument-position `impl Trait` behaves like an anonymous generic parameter:

```rust
fn print_label<T: std::fmt::Display>(value: &T) { /* ... */ }
```

The named form is required when the type must appear elsewhere in the signature, when callers need explicit turbofish selection, or when several arguments must share one type.

```rust
fn same_type<T: Display>(left: T, right: T) { /* ... */ }
```

Two separate `impl Display` arguments may be different concrete types. This difference is semantic.

#### Public API consideration

Changing between a named generic parameter and argument-position `impl Trait` can affect how callers specify type arguments and is not always a purely cosmetic public change. Review public signatures rather than assuming equivalence.

#### The function chooses one hidden concrete type

```rust
fn labels() -> impl Iterator<Item = String> {
    ["a", "b"].into_iter().map(str::to_owned)
}
```

Callers know the returned value implements the stated bound but cannot name the hidden concrete iterator type. Every return path must resolve to the same hidden concrete type.

```compile_fail
fn choose(flag: bool) -> impl Display {
    if flag { 1u32 } else { "one" }
}
```

Both types implement `Display`, but they are different hidden types. Use an enum or trait object if run-time branching genuinely selects different concrete representations.

#### Opaque is not dynamic

The compiler still knows the concrete hidden type and dispatch remains static. The caller loses the ability to name or depend on details beyond the bounds. This is abstraction by opacity, not type erasure via a vtable.

#### Bound design

Expose every capability callers need. Adding another bound later may be compatible for existing callers, but removing one is not. Returning an opaque type can also make testing or composition harder when callers need concrete traits not stated in the signature.

#### A trait method can return an opaque implementor

Modern stable Rust supports return-position `impl Trait` in trait methods for many uses:

```rust
trait Labels {
    fn labels(&self) -> impl Iterator<Item = &str>;
}
```

Each implementation chooses one hidden concrete return type satisfying the bound.

#### Design consequences

- callers cannot name the return type;
- the chosen bounds become the usable public contract;
- the method is not dyn-compatible because opaque return types are excluded from dispatchable trait-object methods;
- downstream trait implementors may be constrained by future bound changes.

An associated type can be preferable when callers must name, further constrain, or relate the returned type:

```rust
trait Labels {
    type Iter<'a>: Iterator<Item = &'a str>
    where Self: 'a;
    fn labels(&self) -> Self::Iter<'_>;
}
```

This is more explicit and more complex. Choose according to caller needs, not novelty.

#### Generated instances

A generic function may produce machine-code instances for concrete type combinations used by the program. This supports optimization with concrete knowledge but can increase compile time and binary size.

#### Avoid folklore

Do not claim that static dispatch is always faster or that trait objects are slow. Real cost depends on call frequency, inlining, code locality, branch prediction, allocation, and workload. Course 9 measures those claims.

#### Architectural cost before runtime cost

Generic types propagate through signatures and can produce difficult diagnostics. Changing a strategy type changes the enclosing concrete type. Public generic APIs expose implementation choices and can increase downstream compile work.

#### Boundary pattern

A common architecture uses static composition inside a subsystem and erases at a stable outer boundary—or the reverse, dynamic runtime components inside a generic source/reporter shell. The capstone uses both and requires a reason for each boundary.

Three validators are selected in source code and never change at run time. A tuple-composed generic pipeline preserves their concrete types and can require each to implement `Validate<Input = Submission>`.

Introducing `Vec<Box<dyn Validator>>` would support runtime heterogeneity the product does not need, force associated types to be fixed, and erase concrete configuration. The static pipeline is appropriate.

When a policy file later chooses an arbitrary list of built-in rule kinds, the requirement changes. That is the point at which dynamic dispatch becomes justified—not before.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For design generic functions and types with the weakest sufficient bounds, construct one positive and one causal negative example. Mark the first decisive fact in the **static-dispatch map** and state which evidence could falsify the claim.

2. **Outcome 2.** For distinguish argument-position and return-position `impl Trait`, construct one positive and one causal negative example. Mark the first decisive fact in the **static-dispatch map** and state which evidence could falsify the claim.

3. **Outcome 3.** For explain monomorphization without promising optimization outcomes, construct one positive and one causal negative example. Mark the first decisive fact in the **static-dispatch map** and state which evidence could falsify the claim.

4. **Outcome 4.** For choose static dispatch when concrete type identity carries useful guarantees, construct one positive and one causal negative example. Mark the first decisive fact in the **static-dispatch map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Keep source and reporter boundaries statically dispatched, using the weakest sufficient bounds and opaque types only where concrete names would leak irrelevant detail. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-04-static-pipeline/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 25 when you can:

- answer the module question—“When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design generic functions and types with the weakest sufficient bounds;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: impl Trait](https://doc.rust-lang.org/reference/types/impl-trait.html)
- [Rust Compiler Development Guide: Monomorphization](https://rustc-dev-guide.rust-lang.org/backend/monomorph.html)

[← Module 23](../../../03-rust-traits-generics-architectural-design/course-book/module-23-coherence-and-implementation-ownership/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 25 →](../../../03-rust-traits-generics-architectural-design/course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md)

## Continue

Continue to [Module 25 — Trait Objects and Dynamic Polymorphism](../module-25-trait-objects-and-dynamic-polymorphism/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
