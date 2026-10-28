# 28 — Boundary Traits and Adapters

**Course 3, day 8 · Module 28 of 60**  
`█████████░░░░░░░░░░░` **28/60**

[← Module 27: Typestate and Capability-Oriented APIs](../module-27-typestate-and-capability-oriented-apis/index.md) · [Course 3 overview](../index.md) · [Sixty-module map](../../../COURSE_MAP.md) · [Module 29: Public API Evolution →](../module-29-public-api-evolution/index.md)

## The question

> How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

## Why this comes now

A well-modeled core still has to meet files, clocks, stores, callbacks, and foreign types. Boundary traits and adapters now provide narrow seams without turning every concrete operation into an interface. Conversion traits are taught as contracts with semantic differences, not interchangeable conveniences.

## What you will be able to do

- Design extension traits, closure adapters, and conversion boundaries with precise contracts.
- Use generic or dynamic ports according to ownership and deployment needs.
- Build test doubles that preserve the production contract rather than mirror internals.
- Recognize visitor, repository, and service abstractions that add more ceremony than leverage.
- Refactor a boundary while preserving the domain core.

## Core model

### Boundaries translate; the core should not know every environment

A well-structured Rust program keeps domain rules independent from files, terminals, clocks, network clients, and third-party data shapes. Traits can define narrow ports at those boundaries, but a trait for every struct creates indirection without variation.

Start with the use case:

```rust
pub trait SubmissionSource {
    type Error;

    fn load(&mut self) -> Result<Vec<Submission>, Self::Error>;
}

pub trait ReportSink {
    type Error;

    fn write(&mut self, report: &Report) -> Result<(), Self::Error>;
}
```

The application service depends on domain-shaped operations. A filesystem adapter owns path handling and decoding. An in-memory fake owns deterministic test data. Neither leaks file handles or test-specific behavior into the domain model.

### Choose static or dynamic ports intentionally

A generic service gives static dispatch:

```rust
struct App<S, R> {
    source: S,
    sink: R,
}
```

This is simple when one application value uses fixed adapter types. It can make type signatures propagate when many layers carry the service.

A boxed port gives dynamic dispatch:

```rust
struct App {
    source: Box<dyn SubmissionSource<Error = AppError>>,
    sink: Box<dyn ReportSink<Error = AppError>>,
}
```

This permits runtime selection and homogeneous storage but requires one erased object surface and usually one normalized error type.

A third option is to keep effects outside the long-lived struct and pass them to a function:

```rust
fn run<S, R>(source: &mut S, sink: &mut R) -> Result<(), RunError<S::Error, R::Error>>
where
    S: SubmissionSource,
    R: ReportSink,
{
    // ...
}
```

Do not default to boxed ports because an architecture diagram says “dependency inversion.” Use the least machinery that preserves substitution and testability.

### Closures are adapters for single operations

A named trait is useful for a multi-method contract or public extension point. A closure is often better when variation is one operation:

```rust
fn evaluate_with<F>(submissions: &[Submission], mut emit: F)
where
    F: FnMut(Finding),
{
    for submission in submissions {
        // ...
        emit(Finding::new(submission.id()));
    }
}
```

The callable bound documents invocation capability. A small adapter can implement a named trait for a closure when storage or API uniformity requires it:

```rust
struct RuleFn<F> {
    id: &'static str,
    f: F,
}

impl<F> Rule for RuleFn<F>
where
    F: Fn(&Submission, &mut Vec<Finding>),
{
    fn id(&self) -> &'static str { self.id }

    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>) {
        (self.f)(input, out)
    }
}
```

This keeps ad-hoc rules concise without making the core registry closure-specific.

### Extension traits add fluent local vocabulary

An extension trait can add a method to foreign or generic types:

```rust
pub trait ResultContext<T, E> {
    fn context(self, message: &'static str) -> Result<T, ContextError<E>>;
}

impl<T, E> ResultContext<T, E> for Result<T, E> {
    fn context(self, message: &'static str) -> Result<T, ContextError<E>> {
        self.map_err(|source| ContextError { message, source })
    }
}
```

Use extension traits for coherent convenience behavior whose target family is clear. Avoid broad “utility” traits with unrelated methods or names likely to collide. If the method needs no receiver-specific discovery, a free function may be clearer.

### Conversion traits have different promises

#### `From` and `Into`

Implement `From<Source> for Target` for infallible, lossless-enough, obvious conversions:

```rust
impl From<TaskId> for u64 {
    fn from(id: TaskId) -> Self { id.get() }
}
```

`Into` is supplied automatically from `From`; generally implement `From`.

Do not use `From` for validation that can fail or for surprising policy choices.

#### `TryFrom` and `TryInto`

Use for checked conversion:

```rust
impl TryFrom<String> for Title {
    type Error = InvalidTitle;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.trim().is_empty() {
            Err(InvalidTitle)
        } else {
            Ok(Title(value))
        }
    }
}
```

The error type is part of the boundary contract.

#### `AsRef`

`AsRef<T>` provides a cheap borrowed view used mainly by generic APIs:

```rust
fn read_text(path: impl AsRef<std::path::Path>) { ... }
```

It is not a general semantic conversion system.

#### `Borrow`

`Borrow<T>` promises that the borrowed form has equivalent equality, ordering, and hashing behavior. Collections use this to look up an owned key with a borrowed key, such as `HashMap<String, V>` by `&str`.

Because the law is stronger, do not implement `Borrow<str>` for a type whose string view compares differently from the owner.

#### `Deref`

`Deref` participates in deref coercion and method lookup. It should model smart-pointer-like access, not arbitrary “convert to inner thing” convenience. Overusing `Deref` can expose methods accidentally and make API boundaries difficult to see.

### Adapters own error translation

External errors should not spread through every domain signature. The adapter can preserve the source while adding context:

```rust
#[derive(Debug)]
pub enum LoadError {
    Io(std::io::Error),
    InvalidRecord { line: usize, message: String },
}
```

Do not flatten all failures into `String`. Do not erase errors into `Box<dyn Error>` unless heterogeneous open-ended failures are a real boundary requirement. Typed conversion enables callers to distinguish retryable I/O from invalid input.

### Test doubles must preserve the same contract

A fake source that never fails does not exercise error behavior. A recording sink that accepts invalid reports may hide a production invariant. Reuse contract tests across production adapters and fakes:

```rust
fn sink_contract<S>(mut sink: S)
where
    S: ReportSink<Error = TestableError>,
{
    // successful write
    // deterministic ordering
    // invalid destination behavior
    // repeated-call semantics
}
```

Mocks that assert every internal call order can make tests brittle. Prefer testing public outcomes and boundary contracts. Record interactions only when the interaction itself is the requirement.

### Refactor boundaries from the outside inward

When separating a monolith:

1. identify the pure domain operation;
2. define domain inputs and outputs;
3. move filesystem/terminal/network details behind one adapter;
4. keep the application orchestration concrete at first;
5. introduce a trait only where a second real adapter or test boundary requires substitution;
6. write contract tests shared by adapters;
7. decide whether the port should be generic, borrowed, or dynamically erased.

This avoids framework-shaped architecture in which every type has an interface before the program has two implementations.

#### Core contract versus convenience

A core trait should remain small. A blanket extension trait can add derived methods:

```rust
trait Rule {
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>);
}

trait RuleExt: Rule {
    fn findings(&self, input: &Submission) -> Vec<Finding> {
        let mut out = Vec::new();
        self.evaluate(input, &mut out);
        out
    }
}
impl<T: Rule + ?Sized> RuleExt for T {}
```

The extension works for concrete and erased rules and does not burden implementors with another required method.

#### Evolution advantage

Convenience methods can evolve separately from the minimal core, though name collisions and blanket-implementation compatibility still matter. Keep semantic laws aligned: `findings` must be exactly the collected output of `evaluate`.

#### Import ergonomics

Document the trait import needed for method syntax. Avoid several extension traits that expose overlapping generic names.

#### Closures can satisfy small behavioral boundaries

Instead of defining a concrete type for every local strategy, a newtype can adapt a closure:

```rust
struct RuleFn<F> { id: RuleId, f: F }

impl<F> Rule for RuleFn<F>
where
    F: Fn(&Submission, &mut Vec<Finding>),
{
    fn id(&self) -> RuleId { self.id.clone() }
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>) {
        (self.f)(input, out)
    }
}
```

#### Why a wrapper?

A closure alone may lack stable identity, documentation, or a local relationship needed by coherence. The wrapper carries domain metadata and controls the implementation.

#### `Fn`, `FnMut`, or `FnOnce`

Choose from call semantics. A rule called repeatedly should normally be `Fn`; a stateful local strategy may require `FnMut`; a one-shot command may be `FnOnce`. The choice affects receivers and trait-object usability.

#### Avoid opaque closures in public errors

Closure types are unnameable and diagnostics can be long. Keep adapters near construction boundaries and expose domain contracts to the rest of the program.

#### Standard traits carry semantics

- `From<T>` is expected to be infallible and value-preserving in the intended domain.
- `TryFrom<T>` represents checked conversion.
- `AsRef<T>` provides cheap reference-to-reference conversion.
- `Borrow<T>` carries stronger equivalence expectations used by generic containers, including equality and hashing consistency.
- `Into<T>` and `TryInto<T>` follow from corresponding implementations.

Do not implement a familiar trait merely because the signature fits.

#### Domain constructors may be clearer

`UserId::parse` can communicate validation better than a surprising `TryFrom<String>`, though both may coexist. Avoid chains of generic `Into` bounds that accept semantically inappropriate values.

#### Boundary normalization

Convert foreign representations into validated domain types once at the boundary. Domain code should not repeatedly parse strings or interpret maps.

#### A port is a consumer-owned boundary contract

A domain service may need to load and save submissions without depending on files:

```rust
trait SubmissionStore {
    type Error;
    fn load(&self, id: SubmissionId) -> Result<Option<Submission>, Self::Error>;
    fn save(&mut self, submission: &Submission) -> Result<(), Self::Error>;
}
```

#### Generic port

`Service<S: SubmissionStore>` retains error and implementation types. It is suitable when one store is chosen for the service instance.

#### Dynamic port

`Box<dyn SubmissionStore<Error = StoreError>>` enables runtime replacement or heterogeneous ownership but requires one fixed error type and dyn-compatible methods.

#### Concrete port

If the application has one storage implementation and no independent test or deployment variation, a concrete repository may be simpler. A port is not mandatory architecture.

#### Consumer ownership

Define the contract around what the domain consumer needs, not every method the infrastructure type happens to offer.

#### A fake should implement the public semantics

An in-memory store can be a useful fake if it preserves key laws: ID uniqueness, missing-value behavior, deterministic order, and error timing. A mock that only records method calls may couple tests to implementation sequence rather than outcomes.

#### Contract test suite

Write reusable tests for every store implementation:

```rust
fn store_contract<S>(mut store: S)
where
    S: SubmissionStore<Error = StoreError>,
{
    // save, reload, replace, missing ID, and failure guarantees
}
```

Real implementations may require setup adapters, but the laws should be shared.

#### Deliberate failure injection

A fake can expose controlled failure points to test failure atomicity. Those controls belong to the fake type, not the production trait, unless production callers genuinely need them.

#### Repository

Useful when persistence is independently variable and domain operations need a stable aggregate-oriented contract. Harmful when it wraps every database operation with identical pass-through methods or returns unmodeled maps.

#### Service trait

Useful as a boundary owned by a real consumer. Harmful when every concrete service gets a trait solely for mocking.

#### Visitor

Useful for open operations over a closed element hierarchy in some languages. In Rust, an enum plus exhaustive match or ordinary trait methods may be clearer. Double dispatch adds substantial ceremony.

#### Dependency injection

Constructor parameters and generic fields already inject dependencies. A container framework is not required. Inject only independently variable collaborators.

#### Pattern test

State the change that becomes local because of the pattern. If no credible change is localized, the pattern may only redistribute code.

#### Start from the domain operation

Suppose policy text currently enters every rule as raw strings. Introduce one parsing boundary that creates validated `PolicySpec` values. Rule factories consume those values; execution never sees file lines.

#### Error translation

Infrastructure errors should retain source detail while becoming meaningful at the application boundary. Do not turn every error into `String` merely to unify a trait object.

#### Adapter placement

Keep adapters near the boundary they translate. A TSV adapter belongs near input, not in the domain module. A closure adapter belongs near rule construction.

#### Test layers

- domain tests use concrete values;
- port contract tests exercise implementations;
- adapter tests verify translation and errors;
- application tests verify orchestration;
- CLI tests verify process behavior.

Traits should support these responsibility boundaries, not dictate them.

The engine produces a `Review`. One CLI writes text to stdout, tests want a `String`, and a future file command may write TSV.

A generic `Reporter` with associated `Output` and `Error` preserves caller-specific output. An extension method can report into a `String`. A trait object would force output and error unification and is unnecessary because one reporter is chosen per engine.

A `Write`-based concrete reporter may be even simpler if all outputs are bytes. The design chooses `Reporter` only when report semantics vary independently from byte destination.

### Design a boundary by translating obligations, not by mirroring a library

A boundary trait is valuable when the application needs a stable capability that several adapters can provide. It is not valuable merely because an external SDK has a type with many methods. Start from one application operation and write the obligations on each side:

| Side | Questions |
|---|---|
| application core | What information and effect are actually required? Which error distinctions affect a decision? |
| adapter | How are external values validated, normalized, and translated? Which retries or ordering guarantees exist? |
| external system | Which lifecycle, rate, ownership, or thread rules remain outside Rust’s type system? |
| test substitute | Which semantic laws must a fake preserve so tests do not prove a different system? |

This yields ports that are smaller than the external API and adapters that own the mismatch. Returning the vendor’s error type from the core leaks volatility inward. Erasing every external distinction into `String` loses decision-relevant meaning. Translate errors into the smallest application vocabulary that preserves the behavior the core needs.

#### Closure adapters are useful for one-operation ports

A trait with one operation can often accept a closure through a blanket implementation. The callable bound must match the invocation contract: `Fn` for shared repeated calls, `FnMut` for stateful sequential calls, or `FnOnce` for consumption. Do not add `Send`, `Sync`, or `'static` unless the architecture actually crosses a thread or storage boundary.

#### Conversion traits carry semantic promises

`From<T>` says the conversion is infallible and value-preserving under the API’s model. `TryFrom<T>` says validation may reject the source. `AsRef<T>` provides a cheap borrowed view chosen by the source type. `Borrow<T>` is stronger: owned and borrowed forms must behave equivalently for equality, hashing, and ordering, which is why it supports heterogeneous map lookup. Choosing among them by signature convenience can create incorrect generic APIs.

#### Fakes must implement the same laws

A fake port that returns canned success for every input can make the core look correct while ignoring ordering, duplicate, failure, or idempotency rules. Reusable contract tests should run against production adapters where feasible and against fakes. The substitute may be simpler internally, but it must not redefine the behavior being tested.

#### Budget every abstraction boundary

For each port, record the number of production implementations, test implementations, call sites, translated error variants, and external concepts hidden. A trait with one implementation and no substitution pressure may be premature. A port with dozens of mirrored methods is probably an SDK copy. The ideal boundary is narrow enough to explain in one paragraph and rich enough to protect a real application decision.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Add narrow ports, production adapters, fakes, and conversion boundaries. Each trait must correspond to a real substitution need rather than a desire to mock everything. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-08-boundary-ports/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 29 when you can:

- answer the module question—“How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Design extension traits, closure adapters, and conversion boundaries with precise contracts;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [std::convert](https://doc.rust-lang.org/std/convert/)
- [AsRef](https://doc.rust-lang.org/std/convert/trait.AsRef.html)
- [Borrow](https://doc.rust-lang.org/std/borrow/trait.Borrow.html)

[← Module 27](../../../03-rust-traits-generics-architectural-design/course-book/module-27-typestate-and-capability-oriented-apis/index.md) · [sixty-module map](../../../COURSE_MAP.md) · [Module 29 →](../../../03-rust-traits-generics-architectural-design/course-book/module-29-public-api-evolution/index.md)

## Continue

1. Complete the [Module 28 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 28 — Boundary Ports](../../labs/module-08-boundary-ports/README.md) from its public contract.
3. Apply the Module 28 increment in the [Review Engine engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
