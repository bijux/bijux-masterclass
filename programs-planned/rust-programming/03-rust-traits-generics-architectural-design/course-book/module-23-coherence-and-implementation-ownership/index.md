# Module 23 — Coherence and Implementation Ownership

**Course 3 · Day 3 · Module 23 of 100**
`██████░░░░░░░░░░░░░░░░░░░` **23/100**

[Program](../../../README.md) · [Course 3](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-03-coherence-adapters/README.md) · [Review Engine guide](../capstone.md)

[← Module 22: Associated Types and Type Families](../module-22-associated-types-and-type-families/index.md) · [Module 24: Static Polymorphism and Opaque Types →](../module-24-static-polymorphism-and-opaque-types/index.md)

## The question

> Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?

## Why this comes now

Once implementations become generic, two seemingly reasonable `impl` blocks can overlap or claim a relationship no crate owns. Coherence is therefore taught before sophisticated dispatch. It forces architectural ownership decisions—newtype, extension trait, sealing, or local adapter—rather than compiler-driven improvisation.

### Prerequisite bridge

Module 22 established **Associated Types and Type Families**. Before continuing, verify that you can write law-oriented tests for a type-family abstraction. This module preserves that capability and adds the ability to predict whether an implementation satisfies coherence and orphan rules. Module 24, **Static Polymorphism and Opaque Types**, will rely on both when it asks: *When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?*

### Scope boundary

This module owns the reasoning for **coherence and implementation ownership** inside Course 3. The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- Predict whether an implementation satisfies coherence and orphan rules.
- Detect overlapping blanket implementations and downstream compatibility hazards.
- Use a newtype to establish local implementation ownership.
- Design sealed and extension traits deliberately.
- Produce an implementation-ownership map for a public API.

## Core model

### Coherence gives every implementation one unambiguous owner

Rust must be able to determine which implementation applies without depending on crate-link order or global registration. The coherence rules enforce that requirement. The practical principle is:

> A crate may add an implementation when it owns enough of the relationship to make that implementation its responsibility.

For an implementation `impl Trait for Type`, the simple working table is:

| Trait | Type | Ordinary result |
|---|---|---|
| local | local | allowed |
| local | foreign | allowed |
| foreign | local | allowed |
| foreign | foreign | rejected |

The exact Reference rules contain details about uncovered type parameters and fundamental types, but this table explains most application design decisions.

The rejected quadrant prevents two unrelated crates from both deciding how `ForeignTrait` should apply to `ForeignType`. Without this rule, adding a dependency could create an ambiguous or behavior-changing implementation.

### The orphan error is an ownership signal

Suppose your crate uses a third-party `ExternalId` and wants to implement `Display` for it. Both the trait and type are foreign, so this is rejected:

```rust,compile_fail
impl std::fmt::Display for external::ExternalId {
    // ...
}
```

The strongest repair is often a newtype:

```rust
use std::fmt;

pub struct DisplayId(external::ExternalId);

impl DisplayId {
    pub fn new(inner: external::ExternalId) -> Self {
        Self(inner)
    }

    pub fn into_inner(self) -> external::ExternalId {
        self.0
    }
}

impl fmt::Display for DisplayId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "id:{}", self.0.as_u64())
    }
}
```

The newtype is not bureaucratic wrapping. It creates a local semantic type whose formatting policy your crate owns. It can also validate construction, control conversions, and prevent raw external identifiers from crossing a boundary accidentally.

An extension trait is another repair when the desired behavior is a convenience method rather than participation in a foreign trait:

```rust
pub trait ExternalIdExt {
    fn display_key(&self) -> String;
}

impl ExternalIdExt for external::ExternalId {
    fn display_key(&self) -> String {
        format!("id:{}", self.as_u64())
    }
}
```

Because the extension trait is local, the implementation is legal. Callers opt into the method by importing the trait.

Choose a newtype when you need a distinct domain type or a foreign-trait implementation. Choose an extension trait when the original type should remain the public type and you are adding local convenience behavior.

### Blanket implementations are global claims

A blanket implementation applies to a family of types:

```rust
trait Describe {
    fn describe(&self) -> String;
}

impl<T> Describe for T
where
    T: std::fmt::Display,
{
    fn describe(&self) -> String {
        self.to_string()
    }
}
```

This claims the `Describe` implementation for every present and future `T: Display`. Your crate can no longer add a more specific `Describe` implementation for one such type on stable Rust because it would overlap.

Before publishing a blanket implementation, ask:

1. Is the semantic behavior truly correct for the entire family?
2. Could a type in the family reasonably need different behavior?
3. Does the implementation prevent downstream crates from implementing the trait for their own types?
4. Could a future standard-library or dependency implementation create overlap?
5. Is a helper function or extension method more honest?

Blanket implementations are not merely code reuse. They spend coherence space.

### Overlap is checked from type relationships, not intent

These implementations overlap:

```rust,compile_fail
trait Render {
    fn render(&self) -> String;
}

impl<T: std::fmt::Display> Render for T {
    fn render(&self) -> String { self.to_string() }
}

impl Render for String {
    fn render(&self) -> String { self.clone() }
}
```

`String` implements `Display`, so both apply. Rust does not select the “more specific” implementation as languages with specialization might. Stable Rust requires one unambiguous implementation.

A repair may be:

- remove the blanket implementation;
- wrap the special case in a newtype;
- use separate traits for distinct semantics;
- make the variation an ordinary value or strategy;
- move customization into a method parameter.

Do not encode policy into overlapping type families that the language cannot distinguish.

### Sealing reserves implementation ownership

Sometimes a public trait should be callable by downstream users but implementable only by your crate. A sealed trait uses a private supertrait:

```rust
mod private {
    pub trait Sealed {}
}

pub trait BuiltInRule: private::Sealed {
    fn code(&self) -> &'static str;
}

pub struct LengthRule;

impl private::Sealed for LengthRule {}
impl BuiltInRule for LengthRule {
    fn code(&self) -> &'static str { "length" }
}
```

Downstream crates can use `BuiltInRule` in bounds but cannot implement the inaccessible `private::Sealed` prerequisite.

Sealing is appropriate when:

- exhaustive knowledge of implementors is part of correctness;
- future trait items may need to be added without breaking third-party implementations;
- implementations rely on invariants not expressible in the public trait;
- the trait is a public vocabulary for built-in types, not an extension point.

It is inappropriate when third-party implementation is the product feature. Be explicit in documentation; a public trait that appears extensible but is secretly sealed creates frustration.

### Extension traits are scoped vocabulary

An extension trait adds methods to types satisfying a bound:

```rust
pub trait IteratorAuditExt: Iterator + Sized {
    fn count_ok<T, E>(self) -> usize
    where
        Self: Iterator<Item = Result<T, E>>,
    {
        self.filter(Result::is_ok).count()
    }
}

impl<I: Iterator> IteratorAuditExt for I {}
```

This is a common and useful blanket implementation because the extension trait is local and the method is defined for the entire intended family. Still review naming, import ergonomics, and collision risk. If two extension traits export the same method name, callers may need fully qualified syntax.

Do not use extension traits to hide a poor domain boundary. A free function may be easier to discover and less likely to collide. An inherent method is preferable when you own the type and the behavior is central.

### Coherence is a public-API concern

Publishing a trait decides who can implement it. Publishing a blanket implementation decides which implementation slots remain available. Publishing a newtype decides whether your crate owns a domain distinction. These choices can be difficult to reverse without breaking downstream code.

A coherence review should record:

- which crate owns the trait;
- which crate owns each important type;
- whether downstream implementation is intended;
- every blanket implementation and the family it occupies;
- newtypes that create local semantic ownership;
- sealed traits and the reason they are sealed;
- likely future implementations that must remain possible.

This is not abstract language-law trivia. It is dependency-compatible architecture.

#### One applicable implementation

At any call site, Rust must be able to select at most one implementation of a trait for a concrete type. Coherence combines orphan checks and overlap checks to preserve that property across independently compiled crates.

```rust
trait Label { fn label(&self) -> String; }
struct Local(u32);
impl Label for Local { fn label(&self) -> String { self.0.to_string() } }
```

Both trait and type are local, so this crate clearly owns the relationship.

#### Why global uniqueness matters

If two dependencies could each implement `Display` for the same external type, importing both would make ordinary method and formatting behavior ambiguous. Rust rejects the possibility at implementation time rather than resolving it by import order.

#### Coherence is an ecosystem rule

A local program might appear unambiguous today, but public crates must coexist with future versions and downstream implementations. A broad blanket implementation can overlap with code that does not yet exist. This is why coherence feels stricter than a single-project compiler would need.

#### Design consequence

Trait authors and type authors each control part of the implementation space. A crate that owns neither usually needs a local wrapper or local trait. This encourages explicit adapters rather than invisible global reinterpretation.

#### Local trait or local type

The practical first approximation is:

> You may implement a trait for a type when either the trait or an appropriate type in the implementation is local to your crate.

Therefore this is forbidden in an ordinary crate:

```compile_fail
use std::fmt;
impl fmt::Display for Vec<u8> {
    fn fmt(&self, _: &mut fmt::Formatter<'_>) -> fmt::Result { Ok(()) }
}
```

Both `Display` and `Vec` are external.

#### Generic implementations are more nuanced

The reference defines covered and uncovered type parameters and an ordering rule around the first local type. Fundamental wrappers such as references and `Box` participate specially. Do not rely on a slogan when designing a complex public implementation; reduce it and consult the current reference.

#### Ownership interpretation

The type author can implement external traits for the local type. The trait author can implement the local trait for external types. A third party must introduce a local type or trait, making its interpretation explicit.

#### Do not fight the rule

The common correct repair is a newtype:

```rust
struct HexBytes(Vec<u8>);

impl std::fmt::Display for HexBytes {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for byte in &self.0 { write!(f, "{byte:02x}")?; }
        Ok(())
    }
}
```

The wrapper says “these bytes have hexadecimal display semantics,” avoiding a global claim about every byte vector.

#### Convenience consumes implementation space

```rust
trait Describe { fn describe(&self) -> String; }
impl<T: std::fmt::Display> Describe for T {
    fn describe(&self) -> String { self.to_string() }
}
```

This applies to every current and future displayable type. A downstream crate cannot later provide a specialized `Describe` implementation for its own type once that type also implements `Display`, because the implementations overlap.

#### Overlap without current witnesses

Rust considers whether types *could* satisfy both implementations under the trait system, not only whether a concrete type exists in the current crate. Two generic implementations whose bounds are not mutually exclusive are rejected.

```compile_fail
trait Mark {}
trait A {}
trait B {}
impl<T: A> Mark for T {}
impl<T: B> Mark for T {}
```

A type could implement both `A` and `B`.

#### Specialization is not the default answer

Stable Rust does not offer general user-defined specialization as an escape from overlapping blanket implementations. Design non-overlapping wrappers, enums, or explicit dispatch instead.

#### Semver hazard

Adding a blanket implementation in a later library version can break downstream code that already implemented the trait for a local type. Public compatibility review must consider implementation space, not only function signatures.

#### A wrapper creates local ownership

A tuple struct with one field has no automatic semantic meaning, but it creates a new local type:

```rust
struct CsvRow(Vec<String>);
```

The crate may now implement external traits for `CsvRow`, enforce constructors, hide representation, and distinguish it from an arbitrary `Vec<String>`.

#### Newtype versus type alias

```rust
type CsvRowAlias = Vec<String>;
```

A type alias does not create a new type or new implementation ownership. It only supplies another name. Use a newtype when semantic distinction, validation, or trait implementation matters.

#### Delegation is explicit

Newtypes do not automatically inherit methods or trait implementations from the wrapped type. This is beneficial: the wrapper exposes only intended capabilities. Implement `Deref` only when transparent reference behavior is genuinely the contract; do not use it merely to avoid writing forwarding methods.

#### Adapter design

A newtype can reconcile a foreign interface with a local contract:

```rust
struct Trimmed(String);

impl TryFrom<String> for Trimmed {
    type Error = Empty;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        let value = value.trim().to_owned();
        if value.is_empty() { Err(Empty) } else { Ok(Self(value)) }
    }
}
```

The wrapper owns validation and implementation relationships. It also makes the transformed semantics visible in types.

#### A library may want public bounds without public implementations

The sealed-trait pattern uses a private supertrait:

```rust
mod private {
    pub trait Sealed {}
}

pub trait Token: private::Sealed {
    fn text(&self) -> &str;
}

pub struct Word(String);
impl private::Sealed for Word {}
impl Token for Word {
    fn text(&self) -> &str { &self.0 }
}
```

Downstream code can use `T: Token` but cannot implement `Token` because it cannot implement the private prerequisite.

#### Why seal?

- the set of valid implementors is closed by design;
- future required methods may be added with controlled internal updates;
- implementations rely on invariants that cannot be expressed publicly;
- the trait exists for generic organization, not ecosystem extension.

#### Cost

Sealing prevents legitimate downstream adaptation. A user must wrap or request library changes. Do not seal reflexively. State the extension policy in documentation.

#### Partial sealing

Some APIs expose a public extension trait implemented blanketly for a sealed core trait. This gives users convenience methods without granting implementation control over the core contract.

#### Add methods through a local trait

When neither an external trait nor external type can be modified, a local extension trait can add methods:

```rust
trait StrPolicyExt {
    fn is_policy_key(&self) -> bool;
}

impl StrPolicyExt for str {
    fn is_policy_key(&self) -> bool {
        !self.is_empty() && self.bytes().all(|b| b.is_ascii_lowercase() || b == b'-')
    }
}
```

Because the trait is local, implementing it for `str` is allowed.

#### Extension is opt-in by import

Users import the trait to gain method syntax. Name the trait predictably, document its scope, and avoid collisions with likely standard or ecosystem methods.

#### Blanket extension

An extension trait often has a blanket implementation over a prerequisite:

```rust
trait DisplayExt: std::fmt::Display {
    fn in_brackets(&self) -> String { format!("[{self}]") }
}
impl<T: std::fmt::Display + ?Sized> DisplayExt for T {}
```

This reserves the extension trait implementation for all displayable values, which is usually intentional because downstream users consume rather than implement the extension trait.

#### Not a substitute for domain modeling

Adding `OrderExt` to a foreign map type can hide that the program lacks an `Order` domain type. Use extension traits for genuine cross-cutting convenience, not to avoid modeling local concepts.

#### Map the parties

For each public trait, identify:

- the crate defining the trait;
- crates defining intended implementor types;
- whether downstream implementation is supported;
- blanket implementations already occupying space;
- supertraits and associated items implementors must provide;
- object use expected by callers.

This map predicts which future changes are possible.

#### Open trait costs

An open trait cannot safely gain required methods without a breaking release. New blanket implementations may conflict downstream. New supertraits add obligations. Changing associated types or dyn compatibility can invalidate trait-object users.

#### Closed trait costs

A sealed trait protects evolution but limits ecosystem participation. Users may need adapters around their types. The decision should match the product extension model.

#### Local adapters preserve both sides

A newtype lets downstream users adapt a foreign type without asking either original crate to own the interpretation. Good public APIs make such adapters possible by accepting generic bounds or dyn-compatible contracts at clear boundaries.

You need hexadecimal display for `UuidBytes`, a type from another crate, while `Display` is from `std`.

Direct implementation is forbidden because both sides are foreign. Three options:

1. **Free function:** `format_uuid(&UuidBytes) -> String`; simplest when formatting is local.
2. **Local extension trait:** adds `to_hex_string`; useful when method syntax benefits several foreign types.
3. **Newtype:** `HexUuid(UuidBytes)` implements `Display`; best when hexadecimal formatting is a persistent semantic interpretation passed through generic `Display` APIs.

The correct choice depends on whether the interpretation should travel as a type. The orphan rule forces the decision to be explicit rather than global.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For predict whether an implementation satisfies coherence and orphan rules, construct one positive and one causal negative example. Mark the first decisive fact in the **coherence ownership map** and state which evidence could falsify the claim.

2. **Outcome 2.** For detect overlapping blanket implementations and downstream compatibility hazards, construct one positive and one causal negative example. Mark the first decisive fact in the **coherence ownership map** and state which evidence could falsify the claim.

3. **Outcome 3.** For use a newtype to establish local implementation ownership, construct one positive and one causal negative example. Mark the first decisive fact in the **coherence ownership map** and state which evidence could falsify the claim.

4. **Outcome 4.** For design sealed and extension traits deliberately, construct one positive and one causal negative example. Mark the first decisive fact in the **coherence ownership map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The course capstone is **Review Engine**, a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction. Add local adapters, closure-backed rules, and sealed built-in markers without violating coherence. Record which crate owns every implementation relationship. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-03-coherence-adapters/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 24 when you can:

- answer the module question—“Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Predict whether an implementation satisfies coherence and orphan rules;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Implementations](https://doc.rust-lang.org/reference/items/implementations.html)
- [Rust Reference: Trait implementation coherence](https://doc.rust-lang.org/reference/items/implementations.html#trait-implementation-coherence)

[← Module 22](../../../03-rust-traits-generics-architectural-design/course-book/module-22-associated-types-and-type-families/index.md) · [one-hundred-module map](../../../COURSE_MAP.md) · [Module 24 →](../../../03-rust-traits-generics-architectural-design/course-book/module-24-static-polymorphism-and-opaque-types/index.md)

## Continue

Continue to [Module 24 — Static Polymorphism and Opaque Types](../module-24-static-polymorphism-and-opaque-types/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
