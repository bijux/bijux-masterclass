# Module 22 — Associated Types and Type Families

**Course 3 · Day 2 · Module 22 of 100**
`██████░░░░░░░░░░░░░░░░░░░` **22/100**

[Program](../../../README.md) · [Course 3](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-associated-families/README.md) · [Review Engine guide](../capstone.md)

[← Module 21: Traits as Behavioral Contracts](../module-21-traits-as-behavioral-contracts/index.md) · [Module 23: Coherence and Implementation Ownership →](../module-23-coherence-and-implementation-ownership/index.md)

## The question

> When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

## Why this comes now

A trait contract often relates more than behavior: an implementation may choose an item type, error family, constant, or borrowed view. Associated items follow basic traits because you must first see who owns the contract before deciding who chooses each related type.

### Prerequisite bridge

Module 21 established **Traits as Behavioral Contracts**. Before continuing, verify that you can test semantic laws shared by multiple implementations. This module preserves that capability and adds the ability to choose between generic parameters and associated types from relationship cardinality. Module 23, **Coherence and Implementation Ownership**, will rely on both when it asks: *Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?*

### Scope boundary

This module owns the reasoning for **associated types and type families** inside Course 3. The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Choose between generic parameters and associated types from relationship cardinality.
- Use associated constants and associated types without hiding call-site variation.
- Derive a generic associated type from a borrowing family requirement.
- Explain the effect of associated-item choices on dyn compatibility and callers.
- Write law-oriented tests for a type-family abstraction.

## Core model

### Model the relationship before choosing syntax

Associated types and generic parameters both express type relationships. The decisive question is **who chooses the related type, and how many choices may one implementation support?**

A generic parameter is selected at each use:

```rust
trait Convert<T> {
    fn convert(&self) -> T;
}
```

One implementor may provide several implementations:

```rust
struct Measurement(u32);

impl Convert<String> for Measurement {
    fn convert(&self) -> String { self.0.to_string() }
}

impl Convert<u64> for Measurement {
    fn convert(&self) -> u64 { u64::from(self.0) }
}
```

An associated type is selected once by the implementation:

```rust
trait Source {
    type Item;
    type Error;

    fn load(&mut self) -> Result<Vec<Self::Item>, Self::Error>;
}
```

For one `FileSource` implementation of `Source`, there is one `Item` and one `Error`. Callers do not choose them independently; they are part of what that implementation means.

This is relationship cardinality:

- **many choices for one implementor** → a generic parameter may be appropriate;
- **one canonical related type per implementation** → an associated type is usually clearer.

The rule is not absolute. A trait can have both generic parameters and associated types, but each should reflect a real choice boundary.

### Associated types keep families together

The standard `Iterator` trait is the canonical example:

```rust
trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```

A concrete iterator has one item type. If `Iterator<Item>` were generic instead, a type could in principle implement the same trait several times for unrelated item types, and many call sites would need additional type information. The associated type states that item type belongs to the iterator implementation.

In your own APIs, associated error types avoid erasing useful failure information:

```rust
pub trait Decode {
    type Output;
    type Error;

    fn decode(&self, bytes: &[u8]) -> Result<Self::Output, Self::Error>;
}
```

Generic code can preserve both relationships:

```rust
fn decode_nonempty<D>(decoder: &D, bytes: &[u8]) -> Result<D::Output, D::Error>
where
    D: Decode,
{
    decoder.decode(bytes)
}
```

The function does not need one universal error enum or boxed error merely because implementations fail differently.

### Projection names a related type

`D::Output` is shorthand only when Rust can identify the trait unambiguously. The fully qualified projection is:

```rust
<D as Decode>::Output
```

Projection becomes important in complex bounds:

```rust
fn decode_text<D>(decoder: &D, bytes: &[u8]) -> Result<String, D::Error>
where
    D: Decode<Output = String>,
{
    decoder.decode(bytes)
}
```

`Output = String` is an associated-type equality constraint. It does not change the implementation; it selects implementations whose associated family already has that member.

Avoid repeating projections until signatures become unreadable. A local type alias can help inside a module, but public aliases should not obscure the contract.

### Generic associated types describe a borrowed family

Sometimes the related type changes with a lifetime supplied by the caller. A collection that lends views into itself needs a family of view types:

```rust
trait Records {
    type View<'a>
    where
        Self: 'a;

    fn get<'a>(&'a self, index: usize) -> Option<Self::View<'a>>;
}
```

`View<'a>` is not one type. It is a type constructor indexed by `'a`. The `where Self: 'a` relationship says the implementation value must remain valid for the lifetime of the view.

A concrete implementation can return borrowed records:

```rust
struct Lines {
    values: Vec<String>,
}

impl Records for Lines {
    type View<'a> = &'a str where Self: 'a;

    fn get<'a>(&'a self, index: usize) -> Option<Self::View<'a>> {
        self.values.get(index).map(String::as_str)
    }
}
```

Use a generic associated type when the family is real. Do not introduce one to appear advanced. If every view can simply be `&'a T`, an ordinary method may communicate the API more directly.

### Associated constants belong to the contract, not configuration

An associated constant is fixed by the implementation:

```rust
trait Format {
    const MAGIC: &'static [u8];
    const VERSION: u16;

    fn encode(&self, out: &mut Vec<u8>);
}
```

This is appropriate when the constant is an inherent property of the format implementation. It is not appropriate for values that users should configure at runtime, such as a timeout or maximum number of retries. Runtime policy belongs in values.

Associated constants also matter to dynamic dispatch: a trait with an associated constant is not dyn-compatible. That is not an arbitrary inconvenience. A trait object erases the concrete type, while an associated constant is accessed without a receiver and therefore has no ordinary dispatch operation. If dynamic use is required, expose receiver-based behavior or split the static metadata into another abstraction.

### Generic parameters can express input choice

Consider parsing from several source types:

```rust
trait Parse<Input> {
    type Output;
    type Error;

    fn parse(&self, input: Input) -> Result<Self::Output, Self::Error>;
}
```

Here `Input` may be generic because one parser could support `&str`, `&[u8]`, and a token stream through distinct implementations. `Output` and `Error` may remain associated because they are canonical for each parser/input pairing.

The design becomes difficult when every dimension is independently generic:

```rust
trait Transform<Input, Output, Error, Context> { ... }
```

Such a trait may be honest, but often it indicates that several relationships have not been assigned to the correct owner. Ask whether `Context` should be a method parameter, whether `Error` belongs to the implementation, and whether `Output` is truly caller-selected.

### Type families affect object use

A trait object must specify non-generic associated types:

```rust
trait Reader {
    type Item;
    fn read(&mut self) -> Option<Self::Item>;
}

let readers: Vec<Box<dyn Reader<Item = String>>> = Vec::new();
```

The object erases the concrete reader type, not the item type required by callers. Different associated `Item` types cannot inhabit the same `Vec<Box<dyn Reader<Item = String>>>`.

If heterogeneity of output types is required, choices include:

- normalize to one domain enum;
- erase output behind a second trait object;
- use an enum of reader variants;
- move the heterogeneity outside the collection;
- redesign the consumer so it does not require one homogeneous container.

The correct answer depends on what information the caller must retain.

### A relationship table prevents accidental complexity

Before writing the trait, fill in a table:

| Type/value | Chosen by | How often | Known at compile time? |
|---|---|---:|---|
| input type | caller or implementation? | once or per call? | yes/no |
| output type | implementation? | once | yes/no |
| error type | boundary implementation? | once | yes/no |
| borrowed view | caller lifetime | per borrow | yes |
| format version | implementation | once | yes |
| timeout | user configuration | per value | runtime |

Then select syntax. This reverses a common failure mode in which the author chooses associated types because they “look cleaner” and only later discovers that callers needed multiple choices.

#### Ask how many valid relationships exist

Consider conversion:

```rust
trait Convert<T> {
    fn convert(&self) -> T;
}
```

A source value might convert to several target types, so the target is a generic parameter. The same source type can implement `Convert<String>` and `Convert<Vec<u8>>`.

Now consider iteration:

```rust
trait Sequence {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

One `Sequence` implementation has one item type. Making `Item` a generic parameter would permit multiple `Sequence<T>` implementations for the same type and force callers to infer or state which relationship they mean.

#### Decision rule

- Use a **generic parameter** when one implementor may support several relationships and the caller must choose among them.
- Use an **associated type** when each implementation has one canonical related type.
- Use a **generic associated type** when each implementation defines a family indexed by a lifetime or type.

This is not a style preference. It changes inference, coherence, trait-object spelling, and how many implementations are legal.

#### Caller view

```rust
fn first<S>(mut sequence: S) -> Option<S::Item>
where
    S: Sequence,
{
    sequence.next()
}
```

The caller names the item type through projection, `S::Item`, rather than supplying a second generic argument. This keeps the call site focused on the sequence implementation.

#### Counterexample

A serializer might appear to have one output type, but a serializer implementation may support several targets or configurations. Do not choose an associated type merely to reduce angle brackets. Model the actual relationship count.

#### An implementation selects the related type

```rust
trait Source {
    type Item;
    type Error;

    fn load(&mut self) -> Result<Option<Self::Item>, Self::Error>;
}
```

A file source may yield `Record` and `io::Error`; an in-memory source may yield `Record` and `Infallible`. Generic callers can remain abstract over both:

```rust
fn drain<S>(source: &mut S) -> Result<Vec<S::Item>, S::Error>
where
    S: Source,
{
    let mut items = Vec::new();
    while let Some(item) = source.load()? {
        items.push(item);
    }
    Ok(items)
}
```

#### Projection

`S::Item` is shorthand for `<S as Source>::Item` when the trait relationship is unambiguous. The fully qualified form matters when a type implements several traits with associated items of the same name.

#### Bounds on associated types

A caller can require capabilities from the projected type:

```rust
fn load_labels<S>(source: &mut S) -> Result<Vec<String>, S::Error>
where
    S: Source,
    S::Item: ToString,
{
    // ...
    # Ok(Vec::new())
}
```

Place the bound where it is used. Requiring `Item: ToString` on the trait itself would prohibit sources whose items cannot or should not be stringified, even when most consumers do not need that operation.

#### Associated type defaults

Some associated-item defaults remain unstable or have nuanced support; do not design a public API around a feature without checking the pinned compiler and reference. The course uses stable, explicit associated types.

#### Semantic ownership

An associated error type lets each implementation preserve its native failure information. It can also make heterogeneous storage harder because a trait object must fix the associated types. The choice is an architecture decision, not automatically superior to a shared error enum.

#### Constants belong to the implementation relationship

```rust
trait Frame {
    const HEADER_LEN: usize;
    fn payload(&self) -> &[u8];
}
```

Each frame format selects one header length. Callers can use `F::HEADER_LEN` under a bound.

Associated constants are suitable for values that are:

- known at compile time;
- part of the trait–implementor contract;
- the same for every value of that implementing type.

They are not a substitute for ordinary fields. A maximum configured at run time belongs to a value.

#### Contract implications

Adding a required associated constant to a public open trait breaks downstream implementations. Giving it a default may avoid immediate implementation work but still creates a semantic promise. Changing its meaning can be breaking even when types continue to compile.

#### Trait objects

Traits with associated constants are not dyn-compatible. A trait object represents run-time method dispatch; associated constants do not have an object-dispatch mechanism. Separate the object-safe behavior from type-level metadata when both are needed.

```rust
trait Rule {
    fn id(&self) -> &'static str;
}

trait RuleMetadata: Rule {
    const CATEGORY: &'static str;
}
```

Use `Rule` behind `dyn Rule`; use `RuleMetadata` in generic contexts that know the concrete type.

#### Avoid duplicated truth

Do not expose both `const ID` and `fn id(&self)` unless the two surfaces have a clear purpose. If dynamic callers need the value, a method is usually the authoritative contract.

#### A family indexed by a lifetime

Some abstractions return values borrowing from `self`. The returned type changes with the borrow lifetime. A generic associated type (GAT) expresses that family:

```rust
trait LendingRows {
    type Row<'a>
    where
        Self: 'a;

    fn next_row<'a>(&'a mut self) -> Option<Self::Row<'a>>;
}
```

For a parser reusing an internal buffer, `Row<'a>` may be a view borrowing from that buffer for exactly the mutable borrow of the parser.

```rust
struct RowView<'a> { fields: Vec<&'a str> }

struct TsvRows { buffer: String, done: bool }

impl LendingRows for TsvRows {
    type Row<'a> = RowView<'a> where Self: 'a;

    fn next_row<'a>(&'a mut self) -> Option<Self::Row<'a>> {
        if self.done { return None; }
        self.done = true;
        Some(RowView {
            fields: self.buffer.split('\t').collect(),
        })
    }
}
```

The view cannot outlive the borrow that produced it, and the parser cannot be advanced while that view remains live.

#### Why ordinary `Iterator` is insufficient

`Iterator::Item` is one fixed type for the implementation. It cannot change with each borrow of `&mut self`. A lending interface needs a lifetime-indexed item family.

#### Costs

GAT-based APIs increase signature complexity, interact with borrow checking, and are not dyn-compatible when the associated type is generic. Use them only when borrowed output is a real requirement. Returning owned rows is often simpler and may be sufficiently efficient.

#### Design checkpoint

Before introducing a GAT, measure or establish why ownership is unacceptable. “Zero copy” is not automatically a product requirement, and borrowed outputs constrain storage, iteration, and caller control flow.

#### Projecting a type through a trait

Given `S: Source`, the type `S::Item` is a projection. Generic APIs often constrain it:

```rust
fn count_strings<S>(source: &mut S) -> Result<usize, S::Error>
where
    S: Source<Item = String>,
{
    let mut count = 0;
    while source.load()?.is_some() {
        count += 1;
    }
    Ok(count)
}
```

`Source<Item = String>` is an associated-type equality constraint. It narrows the family member to one concrete type.

#### Equality can overconstrain

If the body only needs `Display`, requiring exactly `String` rejects valid item types:

```rust
fn print_all<S>(source: &mut S) -> Result<(), S::Error>
where
    S: Source,
    S::Item: std::fmt::Display,
{
    // ...
    # Ok(())
}
```

Use equality when identity matters, not merely capability.

#### Nested projections

Real APIs can produce clauses such as:

```rust
where
    S: Source,
    S::Item: IntoIterator,
    <S::Item as IntoIterator>::Item: Display,
```

Read from the outside inward: a source yields an item; that item can be converted into an iterator; each iterator element is displayable. If the clause becomes unreadable, introduce a domain-specific helper trait only when it carries semantics, or move complexity behind a concrete adapter.

#### Normalization and compiler messages

The compiler may display fully qualified projections or generated opaque types. Translate them back into the relationship graph before editing bounds. Adding every suggested bound can produce an API that compiles but exposes the wrong responsibilities.

#### Associated types must be fixed for a trait object

A trait object erases the implementing type, but callers still need to know the types appearing in method signatures:

```rust
trait Source {
    type Item;
    type Error;
    fn load(&mut self) -> Result<Option<Self::Item>, Self::Error>;
}

type RecordSource = dyn Source<Item = Record, Error = SourceError>;
```

The associated types are part of the trait-object type. Two sources with different error types cannot inhabit the same `Vec<Box<RecordSource>>` without an adapter that unifies errors.

#### GATs and associated constants

A trait with a generic associated type or associated constant is not dyn-compatible. This is not an arbitrary limitation: a trait object needs one dispatchable interface with enough type information for each call.

#### Split static and dynamic surfaces

A common design is a dyn-compatible core plus generic extension capabilities:

```rust
trait Rule {
    fn evaluate(&self, input: &Record, out: &mut Vec<Finding>);
}

trait TypedRule: Rule {
    type Config;
    const NAME: &'static str;
    fn from_config(config: Self::Config) -> Self
    where
        Self: Sized;
}
```

Runtime execution uses `dyn Rule`; compile-time registration or factory code uses `TypedRule`. The split should reflect real callers, not merely satisfy the compiler.

#### Erasure ledger

Whenever you form a trait object, record which associated types are fixed, which concrete methods disappear, and which generic capabilities are no longer callable. Type erasure is a deliberate loss of information.

#### Associated type chosen only to shorten syntax

If a codec can encode to bytes, text, and a domain tree, `type Output` falsely claims one canonical target. A generic `Encode<T>` or separate named operations may be correct.

#### Generic parameter chosen despite one relationship

`trait Iterator<T>` would allow a type to implement several item relationships and force callers to carry `T`. The standard `Iterator::Item` captures the one-item-type-per-implementation law.

#### GAT used for prestige

A lending API may avoid allocation but can make values impossible to retain across the next call. If callers need to collect rows, owned output is likely the honest contract.

#### Associated error type at a dynamic boundary

Per-implementation errors preserve detail in static code. A heterogeneous runtime registry may need one shared error envelope. Add an adapter at the erasure boundary rather than forcing every internal implementation to discard detail.

#### Associated constant masquerading as configuration

A batch size supplied by a configuration file is not an associated constant. It belongs to the implementing value.

#### Unnamed semantic family

A type alias or associated type named `Output` communicates little. Prefer domain names such as `Record`, `Finding`, `Handle`, or `Row<'a>` when the relationship has meaning.

Requirements:

- a memory source yields owned `Record` values;
- a buffered parser can expose fields borrowing from its current buffer;
- callers may either process one row immediately or collect durable records;
- a runtime registry of sources is not required.

A single trait with `type Item` cannot express both an owned item and a lifetime-indexed borrowed view under one implementation. Three defensible designs exist:

1. **Owned `Source`:** every source yields `Record`. The parser allocates or copies fields. The API is simple and collectable.
2. **GAT lending source:** `type Row<'a>` follows the borrow of `&'a mut self`. Allocation can be reduced, but callers cannot retain a row while advancing.
3. **Two-layer design:** a low-level lending parser plus an adapter that materializes owned records for ordinary callers.

The third design is often strongest: the complex mechanism remains local, and most of the program receives an owned, ergonomic API.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For choose between generic parameters and associated types from relationship cardinality, construct one positive and one causal negative example. Mark the first decisive fact in the **associated-type relationship map** and state which evidence could falsify the claim.

2. **Outcome 2.** For use associated constants and associated types without hiding call-site variation, construct one positive and one causal negative example. Mark the first decisive fact in the **associated-type relationship map** and state which evidence could falsify the claim.

3. **Outcome 3.** For derive a generic associated type from a borrowing family requirement, construct one positive and one causal negative example. Mark the first decisive fact in the **associated-type relationship map** and state which evidence could falsify the claim.

4. **Outcome 4.** For explain the effect of associated-item choices on dyn compatibility and callers, construct one positive and one causal negative example. Mark the first decisive fact in the **associated-type relationship map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Attach item, output, and error families to the implementations that choose them. Use associated types where callers should not select arbitrary combinations. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-02-associated-families/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 23 when you can:

- answer the module question—“When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Choose between generic parameters and associated types from relationship cardinality;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Associated items](https://doc.rust-lang.org/reference/items/associated-items.html)
- [Rust Reference: Generic parameters](https://doc.rust-lang.org/reference/items/generics.html)

[← Module 21](../module-21-traits-as-behavioral-contracts/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 23 →](../module-23-coherence-and-implementation-ownership/index.md)

## Continue

Continue to [Module 23 — Coherence and Implementation Ownership](../module-23-coherence-and-implementation-ownership/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
