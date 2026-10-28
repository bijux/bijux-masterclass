# Module 26 — Composition and OOP-Style Design Without Inheritance

**Course 3 · Day 6 · Module 26 of 100**
`██████░░░░░░░░░░░░░░░░░░░` **26/100**

[Program](../../../README.md) · [Course 3](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-06-composed-renderer/README.md) · [Review Engine guide](../capstone.md)

[← Module 25: Trait Objects and Dynamic Polymorphism](../module-25-trait-objects-and-dynamic-polymorphism/index.md) · [Module 27: Typestate and Capability-Oriented APIs →](../module-27-typestate-and-capability-oriented-apis/index.md)

## The question

> How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?

## Why this comes now

Dispatch alone does not produce architecture. This module translates familiar object-oriented goals—encapsulation, substitution, strategies, adapters, decorators, and stateful commands—into explicit Rust composition. Inheritance is rejected where ordinary ownership and delegation make the relationship clearer.

### Prerequisite bridge

Module 25 established **Trait Objects and Dynamic Polymorphism**. Before continuing, verify that you can identify the information and capabilities lost during type erasure. This module preserves that capability and adds the ability to model encapsulation, substitution, and delegation without class inheritance. Module 27, **Typestate and Capability-Oriented APIs**, will rely on both when it asks: *Which illegal operations can be removed from the API by representing protocol state and authority in types?*

### Scope boundary

This module owns the reasoning for **composition and oop-style design without inheritance** inside Course 3. The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Model encapsulation, substitution, and delegation without class inheritance.
- Apply composition, strategy, adapter, decorator, and command patterns selectively.
- Separate domain state from interchangeable behavior.
- Detect inheritance-shaped trait hierarchies and replace them with smaller capabilities.
- Test composed behavior without coupling tests to concrete collaborators.

## Core model

### Rust supports object-oriented goals without class inheritance

“OOP” can refer to several different goals:

- encapsulating state behind operations;
- substituting implementations behind a contract;
- reusing behavior;
- selecting strategies at runtime;
- representing state-dependent behavior;
- organizing collaborating objects.

Rust supports these goals, but inheritance is not the default mechanism. Data is represented with structs and enums. Shared behavior is expressed through traits, functions, and composition. Dynamic substitution is available through trait objects when it is actually needed.

A direct class transplant often produces one oversized trait, many boxes, hidden downcasts, and fragile initialization. Begin from ownership and variation instead.

### Encapsulation means one type owns an invariant

Fields are private by default across module boundaries. Use that to ensure all construction and mutation preserve the invariant:

```rust
pub struct Percentage(u8);

impl Percentage {
    pub fn new(value: u8) -> Option<Self> {
        (value <= 100).then_some(Self(value))
    }

    pub fn get(self) -> u8 {
        self.0
    }
}
```

This is stronger than a class with public setters because invalid values cannot be installed after construction. Encapsulation is not about placing every operation inside an `impl`; it is about assigning responsibility for validity.

### Composition makes ownership explicit

Suppose a report needs data, rendering, and delivery. Instead of a base class with virtual hooks, compose collaborators:

```rust
struct Service<S, R, D> {
    source: S,
    renderer: R,
    delivery: D,
}
```

Each field has an owner. Each generic parameter has a contract. The service can be tested with small substitutes. There is no implicit parent state or constructor order.

Composition also permits mixed variation. The source may be a concrete generic for static dispatch, while delivery may be a trait object selected at runtime:

```rust
struct Service<S, R> {
    source: S,
    renderer: R,
    delivery: Box<dyn Delivery>,
}
```

Do not force one polymorphism mechanism onto every collaborator.

### Delegation should remain visible

Rust does not automatically inherit methods from fields. A wrapper delegates deliberately:

```rust
trait Render {
    fn render(&self, input: &Document) -> String;
}

struct Timed<R> {
    inner: R,
}

impl<R: Render> Render for Timed<R> {
    fn render(&self, input: &Document) -> String {
        let started = std::time::Instant::now();
        let output = self.inner.render(input);
        eprintln!("rendered in {:?}", started.elapsed());
        output
    }
}
```

The wrapper preserves the contract and adds behavior. This is a decorator through composition. The implementation should state whether logging, metrics, retries, caching, or synchronization changes error semantics or timing guarantees.

Boilerplate delegation is sometimes the honest cost of a clear boundary. A macro can reduce repetitive syntax later, but first verify that the wrapper truly preserves each delegated operation.

### Strategy is selected behavior

A strategy may be represented in several ways.

#### Generic strategy

```rust
struct Sorter<C> {
    compare: C,
}
```

Use when one concrete strategy belongs to one value and is selected statically.

#### Closure strategy

```rust
fn select_by<T, F>(items: &[T], predicate: F) -> Vec<&T>
where
    F: Fn(&T) -> bool,
{
    items.iter().filter(|item| predicate(*item)).collect()
}
```

Use when variation is one operation and does not need a named multi-method contract.

#### Enum strategy

```rust
enum OrderingPolicy {
    Name,
    Score,
    Created,
}
```

Use when alternatives are closed and should be serialized, matched, or documented exhaustively.

#### Trait-object strategy

```rust
struct Processor {
    policy: Box<dyn Policy>,
}
```

Use when implementations are open or runtime-loaded and the object-facing surface is sufficient.

The pattern name does not decide the Rust mechanism. The variation schedule does.

### Adapters translate contracts

An adapter makes one interface satisfy another without changing the adapted type:

```rust
trait Sink {
    type Error;
    fn write(&mut self, message: &str) -> Result<(), Self::Error>;
}

struct WriterSink<W> {
    writer: W,
}

impl<W: std::io::Write> Sink for WriterSink<W> {
    type Error = std::io::Error;

    fn write(&mut self, message: &str) -> Result<(), Self::Error> {
        writeln!(self.writer, "{message}")
    }
}
```

The adapter owns the translation policy: newline behavior, encoding, error conversion, buffering, and flush semantics. It should not be a transparent-looking wrapper that silently changes meaning.

### Decorators add behavior around a stable contract

A decorator is useful when behavior composes orthogonally:

- retries around delivery;
- caching around lookup;
- metrics around evaluation;
- authorization around commands;
- validation around storage.

Order matters. `Retry<Timeout<S>>` is not necessarily equivalent to `Timeout<Retry<S>>`. One times each attempt; the other may time the whole retry operation. Composition makes that order visible in the type and construction code.

### Commands represent requested operations

A command enum is often better than a trait hierarchy when operations are closed:

```rust
enum Command {
    Add { title: String },
    Remove { id: TaskId },
    Rename { id: TaskId, title: String },
}
```

Pattern matching gives exhaustive handling and keeps required data next to each operation.

A command trait can be appropriate when third parties add operations or commands carry complex behavior:

```rust
trait Command {
    type Output;
    type Error;
    fn execute(self, workspace: &mut Workspace) -> Result<Self::Output, Self::Error>;
}
```

Again, open versus closed alternatives decide the mechanism.

### State can be an enum, typestate, or behavior object

The classic State pattern stores a trait object representing current behavior. In Rust, an enum is usually clearer for a closed state machine:

```rust
enum Status {
    Draft,
    Reviewed,
    Published,
}
```

A typestate API is stronger when operations should be unavailable in invalid states and transitions can consume the value. A trait-object state is useful only when state variants are open or each state has substantial independent behavior that must be erased.

Do not use a pattern because its class diagram is familiar. Use the simplest representation that preserves the state-space contract.

### Trait-hierarchy smells

Review a design when you see:

- traits named `Base`, `Abstract`, or `Interface` without a domain contract;
- one trait containing every operation any implementation might need;
- methods returning `Option` only because some implementors cannot support them;
- frequent downcasts;
- empty marker traits used as categories but carrying no type-system purpose;
- deep supertrait chains;
- boxed objects created even when alternatives are closed;
- getters and setters that expose all fields while pretending to encapsulate them;
- constructors whose valid call order is documented but not represented.

The repair is usually decomposition: one invariant-owning type, one small contract per caller, explicit composition, enums for closed alternatives, and typestate only where compile-time state control is worth the type complexity.

#### Encapsulation

Rust modules and field privacy protect invariants. A public type can expose constructors and behavior while keeping representation private. Encapsulation does not require getters for every field.

```rust
pub struct Account {
    balance_cents: i64,
}

impl Account {
    pub fn try_withdraw(&mut self, cents: u64) -> Result<(), InsufficientFunds> {
        let cents = i64::try_from(cents).map_err(|_| InsufficientFunds)?;
        let next = self.balance_cents.checked_sub(cents).ok_or(InsufficientFunds)?;
        if next < 0 { return Err(InsufficientFunds); }
        self.balance_cents = next;
        Ok(())
    }
}
```

#### Polymorphism

Rust offers several forms: enums, generic bounds, opaque types, and trait objects. “Polymorphic” is incomplete until selection time and extension policy are stated.

#### Inheritance

Traits can require supertraits and provide default methods, but they do not inherit stored fields or establish an “is-a” object layout. A trait bound expresses capability, not nominal ancestry.

#### Composition

A type owns or borrows collaborators and delegates selected behavior. Ownership makes lifetimes and replacement rules explicit.

```rust
struct InvoiceService<P, R> {
    pricing: P,
    repository: R,
}
```

The service does not inherit pricing or persistence. It composes them and exposes only domain operations.

#### Identity and state

A Rust struct can have identity in the domain without reference identity. Stable IDs, handles, and ownership are separate from memory addresses. Course 2 established this distinction; do not reintroduce pointer-centric identity through “objects.”

#### Put validation where invalid state enters

A domain type should own invariants intrinsic to itself. External strategy traits should not be able to construct invalid values by writing fields directly.

```rust
pub struct Percentage(u8);

impl Percentage {
    pub fn new(value: u8) -> Result<Self, OutOfRange> {
        (value <= 100).then_some(Self(value)).ok_or(OutOfRange)
    }

    pub fn get(self) -> u8 { self.0 }
}
```

#### Avoid getter-based pseudo-interfaces

A trait with methods for every private field leaks representation and lets external services reconstruct domain logic. Expose operations such as `approve`, `reserve`, or `evaluate`, not raw mutation primitives.

#### Capability-oriented APIs

Give collaborators only the operations they need. A renderer may receive a read-only `DocumentView`; an editor receives an edit session. This is more precise than a large shared “document object” interface.

#### Internal mutability is not public mutability

A type may cache results internally while presenting an observational contract. Document logical effects. Callers should not need to know whether `&self` uses `RefCell`; they need to know whether repeated calls are deterministic and whether reentrancy is allowed.

#### Own the collaborator explicitly

```rust
trait Formatter { fn format(&self, report: &Report) -> String; }

struct Signed<F> {
    inner: F,
    signer: String,
}

impl<F: Formatter> Formatter for Signed<F> {
    fn format(&self, report: &Report) -> String {
        format!("{}\n-- {}", self.inner.format(report), self.signer)
    }
}
```

`Signed<F>` composes formatting and adds behavior. It can remain statically dispatched. A `Signed<Box<dyn Formatter>>` variant is possible when runtime selection is needed.

#### Delegation is not automatic inheritance

Forward only the capabilities that preserve the wrapper's meaning. If every method is blindly forwarded, the wrapper may fail to enforce its new invariant.

#### Ownership choice

- own a collaborator when its lifetime is tied to the composed object;
- borrow it when a caller controls the lifetime and sharing is explicit;
- use `Rc` only when shared ownership is required;
- use a trait object only when concrete type erasure is required.

These are separate decisions.

#### Composition depth

Nested generic decorators can create difficult types. Constructors, aliases, or selective erasure can contain complexity. Do not erase immediately; first decide where the composition becomes a stable run-time boundary.

#### Strategy separates policy from domain state

A pricing calculation may vary without changing an order's invariant model:

```rust
trait DiscountPolicy {
    fn discount_cents(&self, subtotal: u64) -> u64;
}

struct Checkout<P> { policy: P }
```

The policy is a strategy when callers can replace it under one coherent contract.

#### Generic or dynamic strategy

A generic `Checkout<P>` is suitable when one policy type is chosen at construction. `Box<dyn DiscountPolicy>` is appropriate when configuration chooses among heterogeneous policies at run time. An enum is preferable when the product defines a closed set and variant data needs explicit serialization.

#### Strategy smell

A strategy with one implementation, no test boundary need, and no foreseeable selection point may only relocate a function. Keep concrete behavior until variation exists.

#### Semantic laws

All discount policies must preserve domain constraints: discount does not exceed subtotal, output is deterministic for the same policy state, and integer arithmetic cannot overflow. The trait should express or document those laws.

#### Adapter changes interface

An adapter reconciles one contract with another. A newtype often owns the relationship:

```rust
struct LegacyScorerAdapter(LegacyScorer);
impl Rule for LegacyScorerAdapter {
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>) {
        // translate input and output semantics
    }
}
```

The adapter must handle semantic differences, not merely rename methods.

#### Decorator preserves interface and adds behavior

```rust
struct CountingRule<R> {
    inner: R,
    calls: Cell<u64>,
}

impl<R: Rule> Rule for CountingRule<R> { /* delegate and count */ }
```

A decorator should preserve the original contract. Logging, metrics, caching, and authorization can violate semantics if they change ordering, errors, reentrancy, or side effects.

#### Wrapper explosion

A stack of ten decorators can obscure behavior. Some cross-cutting concerns belong at a higher orchestration boundary. Use composition where the behavior truly wraps one call.

#### Static and dynamic decorators

Generic decorators retain concrete type and can optimize composition. Object-based decorators simplify runtime assembly. Selection time again determines the form.

#### Command represents an operation as data or behavior

A closed command enum is often ideal for CLI input:

```rust
enum Command { Add(Item), Remove(Id), List }
```

It supports exhaustive parsing and matching. A `dyn CommandHandler` registry is useful when handlers are runtime extensions and share one stable envelope.

#### State pattern choices

A state machine can be represented by:

- an enum field and exhaustive match;
- separate state objects behind a trait;
- typestate in generic parameters;
- ordinary validated methods on one struct.

The classic object-oriented state pattern uses dynamic state objects. In Rust, an enum is often simpler when states are closed. Typestate is useful when callers benefit from compile-time operation restriction. Module 27 develops that choice.

#### Do not pattern-match patterns

Select the representation from the change model. “We used the State pattern” is not a design defense. State count, transition openness, persistence format, and API audience are the relevant facts.

#### Nominal ladders

```rust
trait Entity {}
trait Resource: Entity {}
trait Document: Resource {}
trait EditableDocument: Document {}
```

Without independent laws and consumers at each level, this is class hierarchy imitation. It burdens implementors and makes generic bounds vague.

#### Prefer capability intersections

```rust
trait ReadText { fn text(&self) -> &str; }
trait ApplyEdit { fn apply(&mut self, edit: Edit) -> Result<(), EditError>; }
```

A caller needing both can write `T: ReadText + ApplyEdit` or define a meaningful combined contract if the conjunction itself has laws.

#### Liskov-style reasoning

Substitution is semantic. An implementation that panics for a valid trait input or weakens postconditions is not substitutable even though it compiles. Rust's type system enforces signatures, not all behavioral laws.

#### Refusal methods

A broad trait whose implementations return “unsupported” for many methods is not a coherent capability. Split the trait or use an enum that makes supported variants explicit.

A report can render as plain text or TSV, optionally with a signature and line numbering.

A class-oriented design might create subclasses for every combination. Rust composition instead separates:

- core format strategy: `Plain` or `Tsv`;
- decorators: `Signed<F>`, `Numbered<F>`;
- report domain data: concrete `Report`;
- runtime selection boundary: enum or `Box<dyn Formatter>` only if configuration requires it.

This avoids a combinatorial subclass matrix. Each wrapper has one responsibility, and the domain type remains independent of presentation.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For model encapsulation, substitution, and delegation without class inheritance, construct one positive and one causal negative example. Mark the first decisive fact in the **composition diagram** and state which evidence could falsify the claim.

2. **Outcome 2.** For apply composition, strategy, adapter, decorator, and command patterns selectively, construct one positive and one causal negative example. Mark the first decisive fact in the **composition diagram** and state which evidence could falsify the claim.

3. **Outcome 3.** For separate domain state from interchangeable behavior, construct one positive and one causal negative example. Mark the first decisive fact in the **composition diagram** and state which evidence could falsify the claim.

4. **Outcome 4.** For detect inheritance-shaped trait hierarchies and replace them with smaller capabilities, construct one positive and one causal negative example. Mark the first decisive fact in the **composition diagram** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Compose parsing, policy, evaluation, and reporting through owned components and adapters. Do not invent an inheritance hierarchy for responsibilities that can be delegated. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-06-composed-renderer/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 27 when you can:

- answer the module question—“How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Model encapsulation, substitution, and delegation without class inheritance;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [The Rust Book: Object-Oriented Features](https://doc.rust-lang.org/book/ch18-00-oop.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

[← Module 25](../../../03-rust-traits-generics-architectural-design/course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 27 →](../../../03-rust-traits-generics-architectural-design/course-book/module-27-typestate-and-capability-oriented-apis/index.md)

## Continue

Continue to [Module 27 — Typestate and Capability-Oriented APIs](../module-27-typestate-and-capability-oriented-apis/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
