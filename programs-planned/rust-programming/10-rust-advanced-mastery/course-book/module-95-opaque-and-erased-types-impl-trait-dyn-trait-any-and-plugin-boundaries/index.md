# Module 95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

**Course 10 · Day 5 · Module 95 of 100**
`████████████████████████░` **95/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-05-erased-validator-registry/README.md) · [AxiomStore guide](../capstone.md)

[← Module 94: Const Generics, Witness Types, and Compile-Time Invariants](../module-94-const-generics-witness-types-and-compile-time-invariants/index.md) · [Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits →](../module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md)

## The question

> When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary?

## Why this comes now

Course 3 compared static and dynamic dispatch. Advanced library design must distinguish several different forms of hiding. `impl Trait` hides one compiler-known concrete type from callers. `dyn Trait` erases potentially many concrete types behind a dyn-compatible interface. Enums preserve a closed set of variants and enable exhaustive matching. `Any` provides type identity and downcasting but almost no behavioral contract. Module 95 makes those choices explicit and connects them to ownership, allocation, object lifetime, diagnostics, code size, and API evolution.

Course 3 introduced static and dynamic polymorphism. This module separates opaque identity, erased behavior, closed variants, and type downcasting so each boundary keeps only the information it needs.

This module is about information loss by design. Opaque types, enums, trait objects, and `Any` all hide something different. The correct choice follows from what callers must still do, who may add implementations, how values are owned, and where mismatch is reported. Starting from “static versus dynamic dispatch” is too late and too narrow.

### Prerequisite bridge

Module 94 established **Const Generics, Witness Types, and Compile-Time Invariants**. Before continuing, verify that you can choose runtime validation when the value is data-dependent, frequently changing, or not worth a new type identity. This module preserves that capability and adds the ability to distinguish opaque return types from trait objects and explain why different branches of `impl trait` must share one hidden concrete type. Module 96, **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**, will rely on both when it asks: *What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?*

### Scope boundary

This module owns the reasoning for **opaque and erased types: impl trait, dyn trait, any, and plugin boundaries** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type
- derive dyn-compatibility requirements from the operations available through erased receivers
- choose borrowed, boxed, reference-counted, or inline-erased ownership according to registry and lifetime requirements
- use enums for closed variation and trait objects for open runtime extension without confusing the two evolution models
- treat `Any` downcasting as an explicit escape hatch with a documented authority and failure policy
- compare static, enum, and dynamic designs through semantics, diagnostics, code size, and extension ownership rather than slogans

## Core model

### The governing model

Build an **erasure ledger** with five columns: concrete identity hidden, operations retained, ownership/lifetime retained, extension authority, and failure location. Every hiding mechanism is evaluated by what survives the boundary, not by a slogan about flexibility or speed.

### 1. Opaque types hide identity while preserving static knowledge

A return-position `impl Trait` lets the function choose one concrete return type and prevents callers from naming it. The compiler still knows the type, can monomorphize its trait operations, and enforces that all return paths resolve to the same hidden concrete type. Opaque types are useful for iterator pipelines and future values whose internal structure should not become public API. They are not heterogeneous containers.

**Test opaque sameness.** Write two return branches with different iterator pipelines. Why does `impl Iterator` hide one type rather than form a union?

### 2. Trait objects erase identity behind a vtable contract

`dyn Validator<Record>` can hold different validator implementations in one registry if the trait is dyn compatible. Calls use a data pointer and dynamic dispatch metadata. Associated types used through the object must be specified where required, generic methods are generally unavailable, and methods that consume an unsized `Self` need an object-safe shape. Design the trait from the operations needed after erasure, not by copying a rich static trait and hoping it becomes object safe.

**Derive dyn compatibility.** For each trait method, ask whether a caller through `dyn Trait` can name the receiver, arguments, return type, and associated types.

### 3. Ownership is independent of dispatch

`&dyn Trait`, `Box<dyn Trait>`, and `Arc<dyn Trait>` all use dynamic dispatch but express different liveness and sharing. A borrowed plugin registry may require all implementations to outlive the registry. A boxed registry owns each plugin uniquely. An `Arc` registry supports shared liveness but adds atomic reference counting. Select ownership first, then dispatch. Dynamic dispatch does not inherently require heap allocation if the object is borrowed.

**Choose ownership separately.** Compare `&dyn Validator`, `Box<dyn Validator>`, and `Arc<dyn Validator>` for registry lifetime and sharing requirements.

### 4. Enums preserve closed-world structure

An enum can store several known implementations without erasing variant identity. Dispatch becomes a match that the compiler can optimize, and callers can reason exhaustively when variants are public. The cost is closed extension: adding a variant is controlled by the enum’s defining crate and may affect downstream exhaustive matches. Use an enum when the set is intentionally governed centrally, not merely to avoid vtables.

**Identify the closed world.** If only the defining crate should add storage formats, show why an enum communicates that authority better than a plugin trait.

### 5. Any exposes type identity, not a protocol

Downcasting through `Any` is appropriate for narrowly scoped extension payloads, diagnostics, or host-owned context when behavior cannot be captured in a stable trait. It should not replace a missing domain interface. Every downcast needs an authority: who registered the type, who may request it, what happens on mismatch, and whether version skew is possible. A failed downcast is ordinary control flow at an erased boundary, not an impossible state.

**Constrain downcasting.** State who inserted the `Any` payload, who may request a concrete type, and how version mismatch is represented.

### 6. Erasure changes diagnostics and compatibility

Static bounds produce detailed compile-time errors at composition sites. Trait objects move some incompatibility to registration or runtime behavior but create a smaller stable host interface. Opaque return types protect callers from internal concrete-type changes while preserving static checking. Evaluate the boundary through downstream failure experience as well as runtime cost.

**Locate diagnostics.** Compare an invalid static composition, a rejected registration, and a failed downcast. Which boundary owns each error?

### 7. Hybrid architectures are usually stronger than one universal mechanism

A system can use a GAT-based static codec, an enum for built-in storage formats, `Box<dyn Validator<Record>>` for runtime policy extension, and an opaque iterator return type for query composition. Each mechanism owns one variation axis. Trying to make every component dynamic weakens type relationships; making every component generic can spread implementation types through the whole public API.

**Design the hybrid.** Assign static codec, closed format enum, dynamic validators, and opaque query iterator to four separate variation axes.

### Worked variation map: one store, four extension axes

AxiomStore has several kinds of variation that should not be forced through one abstraction:

| Axis | Who adds choices? | When selected? | Appropriate form |
|---|---|---|---|
| archive version | store maintainers | decode time | private closed enum or dispatch table |
| record codec view family | codec implementation | compile time | generic/GAT relationship |
| validation policy | application assembly | runtime | ordered `Box<dyn Validator>` registry |
| query pipeline shape | library implementation | compile time, hidden from caller | return-position `impl Iterator` |

Making archive versions public trait objects would surrender the store’s authority over persistent compatibility. Making validators an enum would require the store crate to know every future application policy. Erasing the codec behind one object would lose or complicate the lifetime-indexed view family. Returning a named concrete iterator would expose implementation structure that callers do not need.

Ownership must be reviewed separately. The validator registry owns each validator uniquely, so `Box` is sufficient. Replacing it with `Arc` would permit shared liveness but also add atomic reference-counting semantics that no current requirement needs. A borrowed `&dyn Validator` would avoid ownership but force the registry’s lifetime through store construction. The dynamic-dispatch choice does not answer any of those questions.

Downcasting is even narrower. If a host stores `Box<dyn Any>`, it can ask whether a payload has a concrete type, but it cannot validate records without knowing that type’s protocol. `Any` is suitable for host-owned extension context with explicit mismatch behavior, not as a substitute for `Validator`. The design test is simple: if every consumer immediately downcasts and then calls the same conceptual method, the missing abstraction is probably a trait.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Is there one hidden concrete return type? | `impl Trait` | trait object used only to hide an iterator adapter |
| Is runtime open extension required? | `dyn Trait` with deliberate ownership | closed enum presented as a plugin system |
| Is the variant set centrally governed? | enum | type erasure that discards useful exhaustive structure |
| Is only type identity available? | `Any` with explicit downcast policy | downcasting as a replacement for a domain contract |

### A rigorous working procedure

1. List the operations callers need after the boundary and the concrete information they must not depend on.
2. Decide whether the set of implementations is closed, open at compile time, or assembled at runtime.
3. Choose ownership and lifetime independently from dispatch.
4. Check dyn compatibility method by method; do not discover it after designing the whole trait.
5. Define mismatch, duplicate identity, ordering, and downcast policy before constructing the registry.
6. Compare static, enum, opaque, and erased alternatives using diagnostics, compatibility, and measured artifact evidence.

### Failure patterns and principled repairs

Erasure failures begin when the design forgets which information callers still need after hiding the concrete type. Repair them by listing retained operations, ownership, lifetime, error, and downcasting requirements first, then selecting opacity, dynamic dispatch, or explicit tagged representation to preserve exactly that contract.

### Returning two different iterator pipelines as `impl Iterator`

Unify the concrete adapter type, use an enum wrapper, or deliberately erase behind a boxed trait object.

### Adding generic methods to a trait-object interface

Move generic work to a static adapter or accept erased owned inputs.

### Selecting `Arc<dyn Trait>` because dispatch is dynamic

Choose liveness and sharing independently; `Box` or a borrow may be sufficient.

### Downcasting without version or mismatch policy

Name who registered the concrete type, how mismatch is reported, and which compatibility boundary owns it.

### What the compiler cannot decide for you

The compiler can enforce dyn compatibility and one-hidden-type rules. It cannot decide whether runtime extension is worth weaker diagnostics, whether a closed enum is an acceptable governance model, or whether atomic shared ownership is necessary. `Any` proves only concrete type identity at runtime; it does not supply a behavioral protocol.

Erasure is a budget. Spend it only on information callers are intentionally forbidden or unable to use, and preserve stable identity and failure policy around the erased value.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type, construct one positive and one causal negative example. Mark the first decisive fact in the **open and erased variation map** and state which evidence could falsify the claim.

2. **Outcome 2.** For derive dyn-compatibility requirements from the operations available through erased receivers, construct one positive and one causal negative example. Mark the first decisive fact in the **open and erased variation map** and state which evidence could falsify the claim.

3. **Outcome 3.** For choose borrowed, boxed, reference-counted, or inline-erased ownership according to registry and lifetime requirements, construct one positive and one causal negative example. Mark the first decisive fact in the **open and erased variation map** and state which evidence could falsify the claim.

4. **Outcome 4.** For use enums for closed variation and trait objects for open runtime extension without confusing the two evolution models, construct one positive and one causal negative example. Mark the first decisive fact in the **open and erased variation map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Trace the example along two axes: dispatch and ownership. Show which concrete types remain known in the generic path, which are represented by enum variants, and which disappear behind a trait object. Verify that all paths share one semantic oracle before comparing generated artifacts.

```rust
trait Validator<R> {
    fn name(&self) -> &'static str;
    fn validate(&self, record: &R) -> Result<(), String>;
}

struct Registry<R> {
    validators: Vec<Box<dyn Validator<R>>>,
}

impl<R> Registry<R> {
    fn run(&self, record: &R) -> Result<(), String> {
        for validator in &self.validators {
            validator
                .validate(record)
                .map_err(|error| format!("{}: {error}", validator.name()))?;
        }
        Ok(())
    }
}
```

### Trace the example

For each call site, write the concrete value owner, the dispatch mechanism, and the available operations. Then add a method generic over `T` to the trait and explain why a vtable cannot contain one entry for every future `T`. Repair the design by moving generic work outside the erased interface or by using an associated erased operation.

Next, replace `Box<dyn Trait>` with `Arc<dyn Trait>` and state the new liveness and synchronization costs. If no requirement needs shared ownership, revert the change; dynamic dispatch alone did not justify it.

### Use it in AxiomStore

AxiomStore keeps codecs static because their borrowed associated families and representation relationships are compile-time architecture. It keeps validators dynamic because operators assemble policy at runtime and validators consume an owned stable `Record`. Built-in archive versions are represented by an enum because the reader owns that closed compatibility set. Query pipelines return opaque iterators so internal adapter choices remain private.

AxiomStore’s variation map must contain one row per axis:

```text
axis
closed or open set
selection time
identity retained
operations retained
ownership form
failure boundary
compatibility owner
chosen mechanism
```

The reference design uses a static GAT codec, closed built-in format authority, `Box<dyn Validator>` for runtime policy, and ordinary owned `Record` values. Do not erase the codec’s lifetime family merely to make the architecture uniform.

## Practice sequence

1. **Opaque branch repair.** Unify two iterator branches with an enum adapter, boxing, or a common pipeline and compare the contracts.
2. **Dyn-compatibility audit.** Review a trait containing a generic method, associated function, consuming receiver, and associated type. Mark what must change.
3. **Ownership matrix.** Select borrowed, boxed, or `Arc` trait objects for three different registry lifecycles.
4. **Closed/open redesign.** Implement one enum-based built-in set and one dynamic plugin set over the same semantic oracle.
5. **Downcast policy.** Build a small `Any` context with typed insertion, duplicate policy, and explicit mismatch errors; then explain why a trait might be better.

Complete the [workbook](workbook.md) and [Erased Validator Registry](../../labs/module-05-erased-validator-registry/README.md). Compiler investigations must distinguish object-safety rejection from runtime registration or downcast failure.

## Ready to continue

Proceed when you can choose among `impl Trait`, enum, generic parameter, `dyn Trait`, and `Any` from an information-retention table; derive dyn compatibility without trial and error; and justify ownership independently. You should be able to identify one AxiomStore axis that must remain static and one that genuinely benefits from erasure.

## Primary Rust references

- The Rust Reference: impl Trait
- The Rust Reference: dyn compatibility
- The standard library documentation for Any and trait objects

Use the dyn-compatibility and `impl Trait` references to verify exact restrictions. Treat object layout and vtable shape as implementation observations unless a public contract says otherwise.

## Continue

Continue to [Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](../module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
