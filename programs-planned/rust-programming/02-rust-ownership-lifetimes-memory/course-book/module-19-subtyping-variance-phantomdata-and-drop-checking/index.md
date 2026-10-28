# 19 — Subtyping, Variance, PhantomData, and Drop Checking

**Course 2, day 9 · Module 19 of 90**  
`██████░░░░░░░░░░░░░░` **19/90**

[← Module 18: Memory Representation, Validity, and Layout](../module-18-memory-representation-validity-and-layout/index.md) · [Course 2 overview](../index.md) · [Ninety-module map](../../../COURSE_MAP.md) · [Module 20: Pinning and Address-Sensitive Design →](../module-20-pinning-and-address-sensitive-design/index.md)

## The question

> When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?

## Why this comes now

Generic reference-bearing types can allow or forbid lifetime substitution depending on how their parameters are used. Variance, `PhantomData`, and drop checking now explain those capabilities. The purpose is not type-system ornament; it is to understand which branded handles and ownership markers a public API is actually permitted to expose.

## What you will be able to do

- State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.
- Compose variance through shared references, mutable references, cells, function arguments/results, and generic wrappers.
- Read outlives bounds and destructor use without claiming owned values are borrowed for the bound lifetime.
- Choose PhantomData shapes from ownership, borrowing, variance, auto-trait, and drop-check semantics, while treating current drop-check details as version-sensitive.
- Use higher-ranked generative brands to prevent cross-scope identity mixing and explain why generations remain necessary for slot reuse.

## Core model

### Subtyping as substitutability

For lifetimes in covariant shared-reference positions, a longer-valid reference can be used where only a shorter validity period is required. Rust describes the longer lifetime as a subtype of the shorter lifetime in this relation. Avoid everyday “bigger/smaller type” intuition; use substitution:

> If code requires `&'short T`, may `&'long T` be supplied safely when `'long: 'short`?

Yes, for a covariant shared reference, because the caller can simply stop using it earlier.

### Variance asks how a type constructor preserves substitution

For constructor `F<T>`:

- covariant: subtype relation is preserved;
- contravariant: relation reverses;
- invariant: no substitution in either direction;
- bivariant: unconstrained (rare in meaningful safe fields).

Derive from operations, not tables alone.

#### Shared-reference summary

`&'a T` is covariant in `'a` and in `T` because shared access observes values; shortening a valid borrow or viewing a subtype through a super-requirement is safe under the relevant relation.

#### Mutable references

`&'a mut T` is covariant in the borrow lifetime `'a` but invariant in `T`. It can be reborrowed for a shorter duration, but changing the referent type covariantly would permit writing a shorter-lived value into storage expected to contain a longer-lived one.

A write counterexample is the proof. Suppose `&mut &'static str` could be treated as `&mut &'short str`; code could write a short local reference, then the original storage would falsely contain `&'static str`.

#### Functions

Function argument types are contravariant and return types covariant in ordinary subtype reasoning: a function able to accept a broader set of inputs can stand in for one used with a narrower set; a function returning a more specific/longer-valid result can satisfy a shorter requirement.

### Constructor composition

Trace variance through every constructor. `Cell<T>` is invariant because replacement permits writes. A covariant `Vec<T>` placed behind `&mut` becomes invariant in the complete referent type. A function marker can deliberately create invariance.

### Outlives and drop checking

`T: 'a` constrains borrows contained in `T`. A destructor can read fields at drop, so destruction is a hidden final use and may affect which borrows must remain valid. Safe generic ownership normally communicates this through real fields. Advanced marker/drop-check behavior is subtle and may evolve; follow current standard documentation and avoid memorized “magic spell” tables.

### PhantomData as a semantic field

A zero-sized marker tells the compiler about a relationship not represented by a runtime field. It can affect variance, auto traits, and drop checking. Choose it from the abstraction's semantics:

- does the type logically own `T`?
- borrow `T` shared or exclusively for `'a`?
- require invariance in a brand?
- merely mention a type in a function-like position?

A marker is not decorative. A wrong marker can make a type more or less substitutable or send incorrect auto-trait/drop signals.

### Generative brands

A higher-ranked callback can introduce a fresh invariant lifetime brand:

```rust
pub fn with_arena<R>(operation: impl for<'id> FnOnce(Arena<'id>) -> R) -> R {
    operation(Arena::new())
}
```

Private constructors and an invariant marker prevent IDs from separate invocations from mixing and prevent brand-bearing values from escaping in `R`. The arena still needs bounds checks. If slots are removed/reused, branding alone does not reject a stale ID from the same brand; add generations or prohibit reuse.

Brands prove scope provenance. Generations prove temporal slot validity. They solve different problems.

### Worked derivation: wrapper variance

For:

```rust
struct View<'a, T> {
    value: &'a T,
}
```

`View` is covariant in `'a` and `T`. For:

```rust
struct Slot<'a> {
    value: std::cell::Cell<&'a str>,
}
```

`Cell` makes the contained lifetime invariant because it permits replacement. Derive this by imagining a write of a short reference into a slot assumed longer.

### Derive it yourself

Given a cache handle with a marker and a real `Vec<T>` owner, derive variance and auto-trait implications for three marker choices. Then decide whether a runtime generational handle or a scoped brand matches a CLI-storable identity.

### Misconception clinic

- Lifetime subtype direction is best remembered through substitutability, not “longer is bigger.”
- `&mut T` is invariant in `T`, but its own borrow can be shortened.
- PhantomData has semantic compiler effects.
- Generative brands do not solve stale same-brand reuse.

Rust permits a reference valid for a longer region to be used where a reference valid only for a shorter region is required. The longer lifetime is a subtype of the shorter lifetime in Rust's reference-subtyping relation.

```rust
fn use_briefly<'short>(text: &'short str) -> usize {
    text.len()
}

let owned = String::from("long enough");
let length = use_briefly(&owned);
```

The borrow of `owned` can be shortened to exactly the call/use region. This is safe because a value valid longer is certainly valid during the shorter interval.

### Direction matters

It is tempting to think “shorter is a smaller type and therefore subtype.” For lifetimes, substitutability is the guide:

> Can a reference that remains valid longer stand in for one required only briefly?

Yes. The reverse is not safe.

### Outlives relation versus subtype notation

Rust syntax writes `'long: 'short` to mean `'long` outlives `'short`. This supports the subtype substitution from longer to shorter in covariant positions.

```rust
fn shorten<'short, 'long: 'short>(value: &'long str) -> &'short str {
    value
}
```

The function does not change the referent or extend anything. It exposes the reference under a weaker promise.

### Borrow checker already shortens routinely

Non-lexical lifetime reasoning and reborrowing perform shortening without explicit helper functions. Variance determines whether the containing type permits that substitution.

### Subtyping is not coercion between owners

A `String` does not become another owner because a reference is shortened. An `Rc<T>` clone is ownership, not lifetime subtyping. Keep validity substitution separate from resource topology.

### Why this matters later

When a reference is nested inside `&mut`, `Cell`, a function parameter, or a custom generic wrapper, the outer constructor may preserve, reverse, or forbid the inner subtype relation. Lifetime annotations alone cannot overcome the constructor's variance.

### Practical reading

For an error mentioning that one lifetime “must outlive” another, write:

1. the source reference lifetime;
2. the required destination lifetime;
3. every generic constructor around it;
4. whether each constructor allows shortening.

This turns a punctuation problem into a substitution trace.

Suppose `Sub` can be used wherever `Super` is required. For a type constructor `F<T>`:

- **covariant** means `F<Sub>` can be used as `F<Super>`;
- **contravariant** means `F<Super>` can be used as `F<Sub>`;
- **invariant** means neither substitution is generally allowed;
- **bivariant** means both are allowed, usually only when the parameter is semantically unused.

### Covariance preserves direction

Read-only containers often permit covariance because exposing a more specific/longer-valid value where a less specific/shorter one is required is safe.

### Contravariance reverses direction

A function that can accept a very general input can stand in for one that will be called with a narrower input. Function argument positions are therefore contravariant.

### Invariance blocks substitution

Mutable storage is often invariant because both reading and writing are possible. If a container could be retyped to a shorter reference element and then written with that shorter reference, the original longer-typed container would later expose an invalid value.

### Derive from operations

Do not memorize only shapes. Ask:

- Does the type only produce `T`? Covariance is plausible.
- Does it only consume `T`? Contravariance is plausible.
- Does it both consume and produce `T`? Invariance is likely.
- Is `T` absent except at type level? Marker choice decides.

### Variance composition rules

Variance composes through nesting. Covariant inside covariant remains covariant. Covariant through contravariant reverses. Any invariant layer makes the result invariant for that parameter.

For example, `&'a Cell<T>` is covariant over the outer borrow lifetime `'a`, but `Cell<T>` is invariant over `T`. Therefore changing a lifetime nested inside `T` is blocked even though the reference itself is shared.

### API effect

Variance is inferred from fields and cannot be declared directly for ordinary Rust structs. Choosing field/marker types determines it. A wrapper that stores `PhantomData<&'a mut T>` communicates a different substitution policy from `PhantomData<&'a T>`.

### Soundness connection

Variance becomes critical for unsafe abstractions because incorrect substitution can create dangling references. This course stays safe but prepares the ability to audit such contracts before Course 6 permits implementation.

### Shared-reference derivation

`&'a T` is covariant over `'a` and covariant over `T` (subject to `T: ?Sized`). It only provides shared observation, so shortening the borrow or viewing a subtype as a supertype is safe.

```rust
fn accept_short<'short>(_: &'short str) {}
let literal: &'static str = "static";
accept_short(literal);
```

### Mutable references: lifetime versus referent

`&'a mut T` is covariant over `'a` but invariant over `T`.

The lifetime may be shortened because exclusive access valid longer can be lent for a shorter period. The referent type cannot be substituted freely because a mutable reference both reads and writes `T`.

### Why invariance over `T` is necessary

Imagine allowing:

```text
&mut &'static str  ->  &mut &'short str
```

Through the shorter view, code could store a short-lived reference into the location. When the mutable borrow ends, the original location would still be typed as `&'static str` but contain a dangling short reference. Invariance prevents this.

A concrete safe compiler rejection demonstrates the rule:

```rust,compile_fail
fn overwrite<'short>(slot: &mut &'static str, short: &'short str) {
    *slot = short;
}
```

No annotation can make `short` static.

### Reborrowing is not referent covariance

Passing `&mut T` into a function for a shorter call creates a shorter reborrow of the same `T`. This uses lifetime covariance/reborrowing, not a change from one `T` to another.

### Nested references

For `&'outer mut &'inner str`:

- outer lifetime can be shortened;
- the inner `&'inner str` sits in the invariant `T` position of `&mut T`, so its lifetime cannot be substituted through that mutable layer.

Write the constructors from outside inward when diagnosing.

### Slices and vectors

`Vec<T>` is covariant over `T` because mutation requires `&mut Vec<T>`, whose mutable-reference layer protects substitution. But `&mut Vec<&'a str>` becomes invariant over the vector's full `T` through the `&mut` layer at the call boundary. Distinguish the type constructor's variance from the variance of a borrowed access to it.

### Receiver design

A method taking `&mut self` can create invariant constraints across generic fields. Sometimes consuming `self`, returning a new value, or separating read/write phases gives a more usable contract.

### `Cell<T>` and `UnsafeCell<T>`

Interior-mutability containers are invariant over `T`. They can replace a value through shared access, so covariance would allow the same short-reference injection problem as mutable references.

`RefCell<T>` is likewise invariant over `T`; runtime borrow checking controls aliasing at access time but does not change type substitution safety.

### Function pointers and callable types

For a function type `fn(A) -> R`:

- argument `A` is contravariant;
- return `R` is covariant.

A function that accepts any short-lived reference can be used where a caller will supply only `'static` references. The reverse is unsafe: a function requiring `'static` cannot accept arbitrary short inputs.

### Example intuition

```rust
fn accepts_any(_: &str) {}
fn invoke_with_static(f: fn(&'static str)) {
    f("literal");
}

invoke_with_static(accepts_any);
```

`accepts_any` is at least as capable as required. It does not demand the argument be static.

### Closure types

Closure variance derives from captured fields and callable trait implementations; it can be less obvious than bare function pointers. Higher-ranked bounds in Module 13 often express the desired input generality more directly.

### Composed example

Consider:

```text
Cell<fn(&'a str) -> &'b str>
```

- function argument reverses `'a`;
- function return preserves `'b`;
- outer `Cell` makes the entire contained type invariant, so both substitution paths are ultimately blocked through the cell.

### Marker design implications

`PhantomData<fn(T)>` can express contravariance without runtime storage; `PhantomData<fn() -> T>` expresses covariance; a shape that uses `T` in both positions can enforce invariance. These markers also have ownership/auto-trait implications that must be reviewed, not selected from a variance table alone.

### Do not optimize API around contravariance trivia

Contravariance appears in callbacks, HRTBs, and marker types. Public APIs should still be written from capability requirements. If a callback must accept any short borrow, say so with `for<'a>` rather than relying on readers to infer subtle coercions.

The bound `T: 'a` means all borrowed data contained within `T` is valid for at least `'a`. It does **not** mean the owned `T` value itself must be stored for `'a`.

```rust
fn hold<'a, T: 'a>(value: T, _witness: &'a ()) -> T {
    value
}
```

For `T = String`, the bound is trivially satisfied for any `'a` because `String` contains no non-static borrow. The local `String` can still be dropped immediately after return usage.

### Reference example

If `T = &'short str`, then `T: 'a` requires `'short: 'a`. The referent must remain valid throughout `'a`.

### Struct well-formedness

A reference-bearing struct:

```rust
struct View<'a, T: ?Sized + 'a> {
    value: &'a T,
}
```

The relation is usually inferred/expressed by the field itself. Explicit outlives bounds may be redundant in modern Rust, but reading them remains essential.

### Drop checking

When a generic value is dropped, its destructor might access generic fields. Rust conservatively ensures borrowed data required by the value remains valid while destruction can occur.

```rust
struct Inspector<'a> {
    text: &'a str,
}

impl Drop for Inspector<'_> {
    fn drop(&mut self) {
        println!("{}", self.text);
    }
}
```

The referent must outlive the inspector's destruction point because the destructor reads it.

### Owning markers

A `PhantomData<T>` field tells the compiler the type acts as though it owns a `T` for variance, drop checking, and related analyses, even though no runtime `T` bytes are stored. This can impose stronger validity requirements than a non-owning pointer marker.

### Destructor assumptions

Unsafe abstractions sometimes promise not to access certain generic parameters during drop, but relaxing drop checking is advanced unsafe territory. Safe course types should model the actual relationship honestly rather than fight the checker.

### Diagnostic question

When an error occurs at end of scope, inspect destruction, not only last explicit use. A value's destructor may be the final use that keeps a borrow relationship alive.

`PhantomData<T>` is zero-sized but tells the compiler that a type behaves as though it contains or relates to `T`. It can affect variance, drop checking, and automatic trait behavior.

### Ownership marker

```rust
use std::marker::PhantomData;

struct OwnerTag<T> {
    id: usize,
    marker: PhantomData<T>,
}
```

This shape acts as though the type owns a `T`, despite storing none. Use it only when that is semantically true—for example, an unsafe owner wrapper represented by a raw handle in a later course.

### Shared-borrow marker

```rust
struct ViewTag<'a, T: ?Sized> {
    index: usize,
    marker: PhantomData<&'a T>,
}
```

This communicates a shared-borrow relationship and is covariant over `'a` and `T`.

### Exclusive/invariant marker

```rust
struct ExclusiveTag<'a, T: ?Sized> {
    index: usize,
    marker: PhantomData<&'a mut T>,
}
```

This is covariant in `'a` but invariant in `T`, reflecting exclusive mutable access to a `T`.

### Function-shaped markers

```rust
struct Produces<T>(PhantomData<fn() -> T>); // covariant in T
struct Consumes<T>(PhantomData<fn(T)>);     // contravariant in T
struct Invariant<T>(PhantomData<fn(T) -> T>); // invariant in T
```

These shapes generally do not claim ownership of an actual `T` in the same way as `PhantomData<T>`, but their full auto-trait/drop implications should be confirmed from official documentation before unsafe use.

### Marker names

Name the field `_marker`, `_brand`, or a domain-specific term, and document what relationship it encodes. A marker selected only to make a compiler error disappear is likely wrong.

### Unused type/lifetime parameters

Rust requires a type parameter to be used in fields so its variance/ownership effect is defined. `PhantomData` is the explicit mechanism when runtime storage is absent.

### Safe-course use

This module uses markers for branded IDs and `PhantomPinned` in Module 20. No raw-pointer owner is implemented. The goal is to state type-level relationships accurately before unsafe abstraction authoring begins later.

A brand is a type-level lifetime token used to prevent values from different scopes/arenas from being mixed even when their runtime representation is identical.

### Brand token

```rust
use std::marker::PhantomData;

#[derive(Clone, Copy)]
pub struct Brand<'id> {
    marker: PhantomData<fn(&'id ()) -> &'id ()>,
}

pub fn with_brand<R>(operation: impl for<'id> FnOnce(Brand<'id>) -> R) -> R {
    operation(Brand { marker: PhantomData })
}
```

The function's HRTB creates a scope whose `'id` is chosen by the function. The invariant function-shaped marker prevents lifetime substitution that could merge brands.

### Branded IDs

```rust
#[derive(Clone, Copy)]
pub struct Id<'id> {
    index: usize,
    marker: PhantomData<fn(&'id ()) -> &'id ()>,
}
```

An arena built within the brand scope accepts only `Id<'id>` from that same scope. Two nested or separate `with_brand` calls create types that cannot be mixed.

### Why the brand cannot escape normally

`R` in `for<'id> FnOnce(Brand<'id>) -> R` is one fixed return type independent of the callee-chosen `'id`. Returning `Id<'id>` directly would require `R` to mention the universally quantified lifetime, so the compiler rejects it.

Owned summaries independent of the brand can escape.

### What branding does not prove

A branded `Id` still needs bounds checks and deletion policy. If the arena reuses indices within the same brand, stale IDs can resolve incorrectly unless generations are included or removal is forbidden. Type-level scope prevents cross-arena mixing, not all temporal staleness.

### Capstone comparison

The capstone's handles must escape function scopes, persist in commands, and detect deletion/reuse. It therefore uses runtime generational handles, not lifetime brands. The lab uses branding to demonstrate a different design point: scoped, non-removing arena access with compile-time non-mixing.

### Ergonomic cost

Brands spread lifetime parameters through types and APIs. Use them when compile-time separation has real value and values naturally remain inside a scope. Do not brand every ID reflexively.

When a lifetime substitution fails:

### Step 1 — Normalize the types

Write the exact source and required destination types, including all references, cells, function types, and markers.

### Step 2 — Establish the base subtype

For lifetimes, record which outlives which. A longer lifetime can substitute for a shorter in a covariant position.

### Step 3 — Walk constructors inside out

For each layer, write:

- covariant: direction preserved;
- contravariant: direction reversed;
- invariant: substitution stops.

### Step 4 — Derive from operations

If unsure, imagine the methods: can the type write `T`, read `T`, or both? Construct the short-reference injection counterexample for mutable storage.

### Step 5 — Inspect drop

A destructor or owning marker may require data valid until destruction even when explicit uses ended.

### Step 6 — Repair the contract

Possible repairs:

- keep lifetimes independent;
- shorten a reborrow rather than retype storage;
- consume and rebuild an owned container;
- avoid storing references; use handles/ranges;
- choose the correct marker shape;
- redesign mutable access around invariant boundaries.

Adding `'static` or using one lifetime name everywhere is not a variance repair.

### Proof artifact

For each difficult case, submit a variance trace such as:

```text
'long <: 'short
&'a T          covariant in T       preserves
Cell<T>        invariant in T       stops
&Cell<T>       outer borrow covariant, inner substitution still stopped
```

A correct trace is more valuable than a memorized table.

A database transaction issues `RowKey<'tx>` values usable only inside that transaction. Keys contain integer indices; a brand prevents cross-transaction mixing.

### Fresh brand

```rust
fn with_transaction<R>(operation: impl for<'tx> FnOnce(Transaction<'tx>) -> R) -> R
```

The callee introduces `'tx`. `R` cannot contain `RowKey<'tx>`.

### Invariant marker

A shared-reference marker is covariant and may permit shortening. Exact transaction identity needs invariance:

```rust
struct RowKey<'tx> {
    index: usize,
    marker: PhantomData<fn(&'tx ()) -> &'tx ()>,
}
```

Argument position is contravariant, return position covariant; combined occurrence is invariant. This marker does not physically borrow a transaction and does not validate stale indices.

### Transaction owner

`Transaction<'tx>` uses the same brand and owns/borrows storage under the scoped API. Constructors for keys remain private. Lookup accepts only `RowKey<'tx>` from the same brand.

### Auto traits and semantics

Marker choice can affect `Send`/`Sync` and drop checking. Function-pointer markers often avoid claiming ownership of `T`; raw-pointer markers have different auto-trait behavior. The design note must state the intended semantics, not only variance.

### Drop-check scenario

If `Transaction` has a destructor that accesses externally borrowed storage, actual reference fields or appropriate marker relationships must keep storage valid through drop. A brand alone does not own backing data.

### Nested proof

Inside transaction A, open transaction B and attempt `b.get(key_a)`. The compile failure proves distinct brands. Also attempt to return `key_a` from the closure. Ensure the errors are lifetime/brand-related.

### Dynamic validity remains

Removing and reusing a row within one transaction can make an old same-brand index stale. Add generations or prohibit deletion. Static branding addresses cross-owner mixing, not temporal reuse.

### When not to brand

Long-lived application IDs, serialization, and cross-component storage often work better with owned keys and runtime validation. Generative lifetimes constrain escape by design. Use them when the entire capability can remain scoped.

### Variance audit

For every wrapper, derive parameters through all fields. An invariant `RefCell<T>` field makes the wrapper invariant in `T` even if other fields are covariant. Never infer variance from naming.

## Use the idea in a complete program

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Review runtime generational handles against a branded alternative. Explain which invalid combinations each technique prevents and which stale-state problem remains runtime data. The exact implementation task is in the [workbook](workbook.md); the full product contract is in the [capstone guide](../capstone.md).

## Practice sequence

1. Reproduce the important examples from this chapter without copying them line for line.
2. Complete the prediction and repair sections in the [workbook](workbook.md).
3. Build the independent [laboratory](../../labs/module-09-variance-branding/README.md).
4. Apply the capstone increment.
5. Open the [reasoned solutions](solutions.md) only after recording your own answer.

## Ready to continue

You are ready for Module 20 when you can:

- answer the module question—“When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?”—without reading the chapter;
- demonstrate this outcome on a fresh example: State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;
- name a simpler alternative and the condition under which you would prefer it.

## Primary Rust references

This chapter is self-contained. These official sources are included for verification and future language updates, not as required reading:

- [Rust Reference: Subtyping and variance](https://doc.rust-lang.org/reference/subtyping.html)
- [PhantomData](https://doc.rust-lang.org/std/marker/struct.PhantomData.html)
- [Rustonomicon: Drop checking](https://doc.rust-lang.org/nomicon/dropck.html)

[← Module 18](../../../02-rust-ownership-lifetimes-memory/course-book/module-18-memory-representation-validity-and-layout/index.md) · [ninety-module map](../../../COURSE_MAP.md) · [Module 20 →](../../../02-rust-ownership-lifetimes-memory/course-book/module-20-pinning-and-address-sensitive-design/index.md)

## Continue

1. Complete the [Module 19 workbook](workbook.md) and freeze every prediction before compiling.
2. Build [Laboratory 19 — Variance Branding](../../labs/module-09-variance-branding/README.md) from its public contract.
3. Apply the Module 19 increment in the [Memory Workspace engineering guide](../capstone.md).
4. Review the [reasoned solutions](solutions.md) only after an independent attempt, then revise the causal model rather than copying code shape.
