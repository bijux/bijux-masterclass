# 25 — Trait Objects and Dynamic Polymorphism

**Course 3, day 5 · Module 25 of 90**  
`████████░░░░░░░░░░░░` **25/90**

[← Module 24: Static Polymorphism and Opaque Types](../module-24-static-polymorphism-and-opaque-types/index.md) · [Course 3 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 26: Composition and OOP-Style Design Without Inheritance →](../module-26-composition-and-oop-style-design-without-inheritance/index.md)

## The question

> When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

## Why this comes now

Static dispatch cannot represent every runtime extension point. Trait objects now introduce deliberate type erasure, heterogeneous storage, object lifetimes, and dyn compatibility. Because the static alternative is already understood, you can justify erasure instead of using `Box<dyn Trait>` by reflex.

## What you will be able to do

- Derive whether a trait is dyn-compatible and repair it without erasing its meaning.
- Use borrowed and owned trait objects with correct object lifetimes.
- Build a heterogeneous runtime collection behind one behavioral interface.
- Compare enum, generic, and trait-object designs against explicit change scenarios.
- Identify the information and capabilities lost during type erasure.

## Core model

### A trait object is an erased value with a dispatchable contract

`dyn Rule` is a dynamically sized trait-object type. It is normally used behind a pointer such as `&dyn Rule`, `Box<dyn Rule>`, `Rc<dyn Rule>`, or `Arc<dyn Rule>`.

Conceptually, a pointer to a trait object carries:

- a pointer to the concrete value;
- metadata that permits dispatch of the trait’s dyn-compatible methods.

This conceptual model explains dynamic method calls. It is not a stable ABI promise about vtable layout or pointer representation. Do not serialize trait objects or depend on metadata order.

```rust
trait Rule {
    fn id(&self) -> &'static str;
    fn check(&self, input: &str) -> bool;
}

struct NonEmpty;

impl Rule for NonEmpty {
    fn id(&self) -> &'static str { "non-empty" }
    fn check(&self, input: &str) -> bool { !input.trim().is_empty() }
}

let rule: Box<dyn Rule> = Box::new(NonEmpty);
assert!(rule.check("data"));
```

The box owns a concrete `NonEmpty`, but callers through `dyn Rule` do not name that concrete type.

### Dyn compatibility is a dispatch question

A trait is dyn-compatible when its object-facing method surface remains meaningful after the concrete `Self` type is erased. Important constraints include:

- the trait as a whole must not require `Self: Sized`;
- all supertraits must be dyn-compatible;
- associated constants are not allowed;
- generic associated types are not allowed on the object-facing trait;
- dispatchable methods cannot have type parameters other than lifetimes;
- dispatchable methods cannot use `Self` outside the receiver type;
- dispatchable methods cannot return opaque `impl Trait` or be `async fn`;
- non-dispatchable methods can be retained with `where Self: Sized`.

The exact current list belongs to the Rust Reference. The reasoning test is: **can a caller invoke this method when the concrete implementing type is unknown?**

A generic method fails that test because one vtable entry cannot represent every monomorphized `T`:

```rust,compile_fail
trait Rule {
    fn check<T>(&self, value: &T) -> bool;
}
```

A method returning `Self` fails because the caller cannot allocate or name the erased result:

```rust,compile_fail
trait CloneRule {
    fn duplicate(&self) -> Self;
}
```

If those operations are useful only on concrete implementations, exclude them from object dispatch:

```rust
trait Rule {
    fn check(&self, input: &str) -> bool;

    fn boxed(self) -> Box<dyn Rule>
    where
        Self: Sized + 'static,
    {
        Box::new(self)
    }
}
```

Do not delete essential behavior merely to make a trait object possible. Split a dyn-facing adapter from a richer static trait when the consumers genuinely need different surfaces.

### Associated types must be fixed at the object boundary

A trait object can use ordinary associated types when the object type specifies them:

```rust
trait Source {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

let sources: Vec<Box<dyn Source<Item = String>>> = Vec::new();
```

The concrete source type is erased, but `Item = String` remains part of the object type because the caller must know what `next` returns.

This is a useful reminder: dynamic dispatch does not mean “all types disappear.” Only information absent from the object-facing contract is erased.

### Object lifetimes describe captured references

A trait object may contain an implementation that borrows data:

```rust
struct Prefix<'a>(&'a str);

impl Rule for Prefix<'_> {
    fn id(&self) -> &'static str { "prefix" }
    fn check(&self, input: &str) -> bool { input.starts_with(self.0) }
}

fn make_rule<'a>(prefix: &'a str) -> Box<dyn Rule + 'a> {
    Box::new(Prefix(prefix))
}
```

`+ 'a` says the erased implementation may contain references valid for `'a`; therefore the trait object cannot outlive that period. It does not say each method borrow lasts for `'a`.

Object-lifetime defaults can infer `'static` in owning contexts. When an implementation borrows non-static data, make the bound explicit rather than adding clones until the error disappears.

### Ownership container and dispatch are separate choices

These types all use dynamic dispatch but have different liveness semantics:

- `&dyn Rule` — borrowed object; another owner controls lifetime;
- `&mut dyn Rule` — borrowed object with exclusive access;
- `Box<dyn Rule>` — one owning handle;
- `Rc<dyn Rule>` — shared ownership within one thread;
- `Arc<dyn Rule + Send + Sync>` — shared ownership suitable for cross-thread use when the implementation satisfies the auto-trait bounds.

Choose the pointer from ownership and concurrency requirements, not because trait-object examples commonly use `Box`.

### Downcasting is an escape hatch, not the normal protocol

Erasure intentionally removes the concrete type. If callers frequently need it back, the trait contract may be missing an operation or the collection may be better modeled as an enum.

`Any` can support controlled downcasting for `'static` types, but it couples consumers to implementation identities and weakens substitutability. Legitimate uses include tooling, registries with optional implementation-specific diagnostics, or transition layers. A core algorithm that downcasts every object is not really using the trait abstraction.

### Enum, generic parameter, or trait object

Use a **generic parameter** when the implementation is selected statically and remains one concrete type:

```rust
struct Engine<R: Rule> { rule: R }
```

Use an **enum** when the set of alternatives is closed and the program benefits from exhaustive matching:

```rust
enum BuiltInRule {
    NonEmpty,
    MaxLen(usize),
}
```

Use a **trait object** when implementations are open, heterogeneous values must share one collection, or runtime configuration chooses the implementation:

```rust
struct Policy {
    rules: Vec<Box<dyn Rule>>,
}
```

An enum often gives better representation of domain variants and can carry variant-specific data. A trait object gives extension without editing the enum, but erases concrete operations and introduces indirect dispatch. A generic gives the strongest static relationships but makes the implementation part of the containing type.

### A sound runtime registry has more than a vector

A useful rule registry must define:

- stable rule identity;
- duplicate-registration behavior;
- deterministic evaluation order;
- ownership of registered rules;
- the object lifetime bound;
- error behavior during construction and evaluation;
- whether rules may hold mutable state;
- whether runtime removal or replacement is supported.

```rust
struct Registry {
    rules: Vec<Box<dyn Rule>>,
}

impl Registry {
    fn register(&mut self, rule: impl Rule + 'static) -> Result<(), DuplicateRule> {
        if self.rules.iter().any(|existing| existing.id() == rule.id()) {
            return Err(DuplicateRule(rule.id()));
        }
        self.rules.push(Box::new(rule));
        Ok(())
    }
}
```

The generic `register` method accepts concrete implementors ergonomically; the registry erases them at the storage boundary. This is a common hybrid architecture: static construction, dynamic storage.

#### A trait object is an unsized erased type

`dyn Rule` represents some concrete value implementing `Rule`, with the concrete type hidden from the caller. It is used behind a pointer such as `&dyn Rule` or `Box<dyn Rule>`.

```rust
fn evaluate(rule: &dyn Rule, input: &Submission) -> Vec<Finding> {
    let mut findings = Vec::new();
    rule.evaluate(input, &mut findings);
    findings
}
```

#### Conceptual implementation model

A trait-object pointer is commonly described as data pointer plus metadata enabling method dispatch. The metadata is often called a vtable. Treat this as an implementation model, not a portable byte-layout or ABI guarantee.

#### Borrowed versus owned objects

- `&dyn Rule` borrows an existing implementor.
- `&mut dyn Rule` permits exclusive dynamic access.
- `Box<dyn Rule>` owns an erased implementor and gives it stable heap indirection, though address stability is not the purpose unless pinning is involved.

Choose ownership independently from dispatch. “Trait object” does not imply `Box` unless the program needs owned heterogeneous values.

#### Not every trait can form a trait object

A dyn-compatible trait must provide a dispatchable method surface whose signatures remain meaningful after the implementing type is erased.

Important restrictions include:

- the trait must not require `Self: Sized` as a whole;
- supertraits must also be dyn-compatible;
- it must not have associated constants;
- it must not have generic associated types;
- dispatchable methods cannot have type parameters other than lifetimes;
- dispatchable methods cannot use `Self` except through the receiver;
- dispatchable methods cannot return opaque `impl Trait` or be `async fn`;
- methods excluded with `where Self: Sized` need not be dispatchable.

Consult the pinned Rust Reference for the exact receiver forms and current rules.

#### Repair by separating surfaces

```rust
trait Rule {
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>);

    fn boxed(self) -> Box<dyn Rule>
    where
        Self: Sized + 'static,
    {
        Box::new(self)
    }
}
```

`evaluate` is dispatchable. `boxed` is a concrete-type convenience method excluded from the trait-object surface.

#### Do not mutilate a contract for object use

If generic methods or associated families are central to the abstraction, splitting a dyn-compatible adapter may be better than weakening the original trait. Dynamic use is one consumer, not the definition of every trait.

#### Why returning `Self` is difficult after erasure

```rust
trait Duplicate {
    fn duplicate(&self) -> Self;
}
```

A caller of `&dyn Duplicate` does not know the concrete return type or its size. The method can remain for concrete implementors with `where Self: Sized`, or the erased interface can return `Box<dyn Duplicate>` through a separate cloning contract.

#### Generic methods require call-time code generation

```rust
trait Encode {
    fn encode<W: std::io::Write>(&self, writer: W);
}
```

A trait object cannot choose a monomorphized implementation for arbitrary `W` through one fixed dispatch slot. Use an erased parameter such as `&mut dyn Write`, move the generic method to an extension trait with `Self: Sized`, or keep static dispatch.

#### Receiver forms

Ordinary receivers such as `&self`, `&mut self`, and `Box<Self>` can support dispatch under the reference rules. Exotic receivers depend on approved pointer forms. Keep public dynamic interfaces simple unless ownership semantics require otherwise.

#### Associated functions

Functions without a receiver cannot be called on a trait object because there is no object selecting an implementation. Mark constructors `Self: Sized` or move them to a factory contract.

#### The hidden implementor may borrow

```rust
struct PrefixRule<'a> { prefix: &'a str }
impl Rule for PrefixRule<'_> { /* ... */ }
```

A boxed object holding this rule cannot outlive the borrowed prefix. The object type may be `Box<dyn Rule + 'a>`.

#### `'static` is not “lives forever”

`Box<dyn Rule + 'static>` means the hidden implementor contains no non-`'static` borrowed data. The box itself can be dropped immediately. Adding `'static` to silence an error may reject useful borrowed implementations.

#### Default object lifetime bounds

Trait objects have default lifetime-bound rules that differ from ordinary elision in some contexts. Write explicit `+ '_` or named lifetimes at public boundaries when the relationship matters.

```rust
fn borrowed_rule<'a>(rule: &'a dyn Rule) -> &'a dyn Rule { rule }
```

#### Ownership and lifetime ledger

For each trait object, record who owns the concrete value and which borrowed data may be hidden inside it. Type erasure hides type identity, not lifetime obligations.

#### Erasure removes concrete capabilities

After converting `ConcreteRule` to `Box<dyn Rule>`, callers can use only the `Rule` surface and auto-trait/lifetime bounds carried by the object. Inherent methods and unrelated trait implementations are no longer directly available.

#### Downcasting is a boundary smell, not always a bug

`Any` can support downcasting for `'static` types, but frequent downcasts usually mean the erased contract is insufficient or the collection should be an enum. Downcasting may be legitimate in diagnostics, plugin registries, or integration boundaries where concrete recovery is an explicit requirement.

#### Prefer explicit introspection

If callers need stable rule identity, include `fn id(&self) -> RuleId` in the contract rather than downcasting to recognize types. If callers need categories, return a domain enum. Expose meaning, not representation.

#### Erasure ledger

For the capstone, record:

- concrete rule type: erased;
- rule identifier: preserved through method;
- configuration type: erased after factory construction;
- evaluation behavior: preserved;
- clone capability: not promised;
- equality and hashing: not promised;
- borrowed data lifetime: preserved in the object bound.

#### Compare against change scenarios

| Question | Enum | Generic | Trait object |
|---|---|---|---|
| Participant set | Closed | Open at compile time | Open at run time within object contract |
| Selection | Run time by variant | Construction/type instantiation | Run time |
| Heterogeneous collection | Natural | No, unless nested/enum | Natural behind pointer |
| Exhaustive matching | Yes | No | No |
| Concrete type retained | Variant known after match | Yes | No |
| Adding participant | Modify enum and matches | Add implementation | Add implementation/factory |
| Dispatch | Branch/match | Static | Dynamic |

#### Closed products often favor enums

If the application supports exactly four rule kinds and every operation needs variant-specific data, an enum may be clearer, easier to serialize, and exhaustively testable.

#### Open runtime registries favor trait objects

If downstream crates or configuration can introduce rule implementations and the executor needs only one stable behavior, `Box<dyn Rule>` is appropriate.

#### Generic strategy when one implementation is selected

A reporter chosen at construction and used uniformly throughout one engine instance is a good generic parameter. A `Vec<Box<dyn Reporter>>` would add unsupported heterogeneity.

Mechanism choice is local. One architecture may use all three at different boundaries.

#### Store owned erased values

```rust
struct Registry {
    rules: Vec<Box<dyn Rule>>,
}
```

The registry owns rules of different concrete types. It should expose operations in terms of the contract rather than leaking `Box` mechanics:

```rust
impl Registry {
    fn push<R>(&mut self, rule: R)
    where
        R: Rule + 'static,
    {
        self.rules.push(Box::new(rule));
    }

    fn iter(&self) -> impl Iterator<Item = &dyn Rule> {
        self.rules.iter().map(Box::as_ref)
    }
}
```

#### Deterministic order

A vector preserves insertion order. If policy order affects finding order, document and test it. A hash-based registry would need explicit sorting for deterministic reports.

#### Factories and construction

Trait objects solve execution heterogeneity, not configuration parsing. Use a factory map or closed parser enum to create concrete rules, validate configuration, then erase them. Keeping construction static preserves typed errors and implementation-specific validation.

#### Avoid object soup

Not every collaborator belongs in a trait-object registry. The capstone keeps source and reporter generic. Only the rule list is truly heterogeneous and selected at run time.

Original contract:

```rust
trait Rule {
    const NAME: &'static str;
    type Config;
    fn new(config: Self::Config) -> Self;
    fn evaluate<T: Record>(&self, input: &T) -> impl Iterator<Item = Finding>;
}
```

Every feature blocks or complicates dynamic execution. Do not erase meaning blindly. Separate construction and execution:

```rust
trait Rule {
    fn id(&self) -> RuleId;
    fn evaluate(&self, input: &Submission, out: &mut Vec<Finding>);
}

trait RuleFactory {
    fn name(&self) -> &'static str;
    fn build(&self, args: &[&str]) -> Result<Box<dyn Rule>, PolicyError>;
}
```

The executor has one concrete input type and output sink, so the core is dyn-compatible. Factories handle typed construction behind their own dynamic or closed registry. A generic `TypedRule` helper may retain associated configuration for built-ins without entering the object surface.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Introduce the ordered heterogeneous rule registry with `Box<dyn Rule>`. Document what is erased, why runtime heterogeneity is required, and how object lifetimes are owned. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-05-dynamic-command-bus/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 26 when you can:

- answer the module question—“When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive whether a trait is dyn-compatible and repair it without erasing its meaning;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Trait objects](https://doc.rust-lang.org/reference/types/trait-object.html)
- [Rust Reference: Dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility)

[← Module 24](../../../03-rust-traits-generics-architectural-design/course-book/module-24-static-polymorphism-and-opaque-types/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 26 →](../../../03-rust-traits-generics-architectural-design/course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md)

## Continue

1. Complete the [Module 25 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 25 — Dynamic Command Bus](../../labs/module-05-dynamic-command-bus/README.md) from its public contract.
3. Apply the Module 25 increment in the [Review Engine engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
