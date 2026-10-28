# Module 93 — GATs, Higher-Ranked Bounds, and Lending Interfaces

**Course 10 · Day 3 · Module 93 of 100**
`███████████████████████░░` **93/100**

[Program](../../../README.md) · [Course 10](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-03-lending-table/README.md) · [AxiomStore guide](../capstone.md)

[← Module 92: Advanced Trait Solving: Goals, Projections, and Type Equality](../module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) · [Module 94: Const Generics, Witness Types, and Compile-Time Invariants →](../module-94-const-generics-witness-types-and-compile-time-invariants/index.md)

## The question

> How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime?

## Why this comes now

Ordinary iterator items do not borrow freshly from the iterator in a way that can vary per call, because `Iterator::Item` is one type for the implementation. Course 2 taught lifetime relationships; Course 3 taught associated families. Generic associated types combine those ideas by allowing an implementation to define a family such as `View<'a>`. Higher-ranked bounds then let a caller state what must hold for every lifetime chosen by the borrow. These mechanisms enable lending interfaces, but they also make lifetime quantification and object-safety limits impossible to ignore.

Course 2 established lifetime algebra and Course 3 established associated families. This module combines them so one trait can describe a family of views indexed by each borrow.

Course 2 taught lifetime relationships and Course 3 taught associated types. GATs combine them: an implementation selects a family of types indexed by a borrow created later. That power changes the consumer protocol. A lent item is not just a cheaper owned item; it may prevent the next call until the current view is released.

### Prerequisite bridge

Module 92 established **Advanced Trait Solving: Goals, Projections, and Type Equality**. Before continuing, verify that you can design generic pipelines whose error and intermediate types remain precise rather than prematurely erased. This module preserves that capability and adds the ability to distinguish one associated type from a lifetime-indexed family of associated types. Module 94, **Const Generics, Witness Types, and Compile-Time Invariants**, will rely on both when it asks: *Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?*

### Scope boundary

This module owns the reasoning for **gats, higher-ranked bounds, and lending interfaces** inside Course 10. The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- distinguish one associated type from a lifetime-indexed family of associated types
- design a lending cursor whose returned view cannot outlive the borrow that produced it
- read `for<'a>` as universal quantification chosen by the caller rather than a long concrete lifetime
- identify when a bound accidentally requires a view for one specific lifetime instead of every usable borrow
- explain why many GAT-heavy traits are not natural trait-object boundaries
- choose between lending, ownership transfer, callback-based access, and copied values according to retention needs

## Core model

### The governing model

Draw a **quantifier-and-borrow map**. For every lifetime parameter, state who chooses it, which value must outlive it, and whether two outputs may coexist. `for<'a>` means the implementation must work for every caller-selected `'a`; a GAT such as `View<'a>` means the implementation supplies a type family whose members are tied to those borrows.

### 1. A GAT defines a family, not one hidden type

`type View<'a>` says that each lifetime argument can select a related type. The implementation may choose `&'a Record`, a parsed view containing several slices, or a guard that keeps internal state borrowed. The required `where Self: 'a` relationship states that the receiver must live long enough for a view derived from it. The family makes provenance part of the trait contract.

**Name the family.** For `type View<'a>`, explain why there is no single hidden `View` type and give two distinct members of the family.

### 2. Lending changes the consumer protocol

With an ordinary iterator, callers may often keep several owned items while continuing iteration. With a lending cursor, the next mutable borrow of the cursor is unavailable while the previous view remains live. That restriction can be exactly what makes zero-copy traversal sound. It is not merely a compiler inconvenience; it is the product protocol produced by reusing one buffer or exposing internal storage.

**Test coexistence.** Retain one row view and attempt another `next`. Which borrow of the cursor is still active, and what redesign permits retained ownership?

### 3. Higher-ranked bounds quantify over caller-chosen lifetimes

A bound like `for<'a> F: Fn(&'a Record)` requires `F` to accept a reference with any suitable lifetime supplied by the caller. It does not mean “choose one very long lifetime.” This distinction matters for callbacks, parsers, and adapters that must not retain temporary views. Universal quantification is a capability: the callee can repeatedly call the function with unrelated short borrows.

**Place the quantifier.** Compare `for<'a> F: Fn(&'a str)` with a function generic over one caller-supplied `'a`. Who chooses the lifetime in each form?

### 4. Quantifier placement changes the API

Compare a function generic over one `'a` selected for the whole call with a bound that must hold for every `'a` produced during repeated access. The first can overconstrain the receiver by coupling all borrows. The second allows each iteration to create a fresh short loan. When a diagnostic mentions a borrow lasting “for all” or effectively requiring `'static`, inspect whether the quantifier was placed on the function, trait, associated family, or callback incorrectly.

**Inspect object use.** Determine whether the lending trait can be used as `dyn Trait` for the required operations. If not, separate static lending from dynamic policy instead of forcing one interface.

### 5. Lending is not always the best public boundary

A borrowing view minimizes copying but restricts storage, mutation, and dynamic dispatch. If clients need to retain records independently, return owned records or provide an explicit `to_owned` step. If only local inspection is needed, a higher-ranked callback can prevent escape with a simpler public surface. If the values are tiny, copying may be clearer and cheaper than a lifetime-rich API. Select the protocol from user behavior, not from a zero-allocation slogan.

**Choose ownership honestly.** For a result that must survive cursor advancement, compare cloning, interning, arena ownership, and an owned conversion method.

### 6. Dyn compatibility remains a separate design question

Traits with generic methods or unresolved associated families are often unsuitable for `dyn Trait`. That does not make them bad traits. It means static lending and runtime erasure solve different variation problems. Keep the GAT-based codec at a static boundary and erase validators or commands at a later owned boundary. Trying to force one trait to serve both can produce complicated wrappers and weaker diagnostics.

**Avoid lifetime contagion.** Identify where AxiomStore can convert a borrowed view into `Record` so storage and policy layers remain lifetime-free.

### 7. Test lifetime contracts with impossible examples

Runtime tests cannot prove that a view fails to escape. Add compile-fail documentation cases showing that a view cannot survive the source or coexist with the next exclusive borrow. Pair them with positive cases that demonstrate the intended local use and explicit ownership conversion. The negative surface is part of the API: it documents which misuse the type system prevents.

**Write a negative contract.** Create a compile-fail example in which a view escapes its snapshot. State exactly which owner is destroyed too early.

### Worked protocol comparison: lending, ordinary borrowing, and ownership

Consider three ways to expose rows from one backing string:

```text
A. Iterator<Item = &'input str>
B. LendingCursor with View<'borrow>
C. Iterator<Item = String>
```

A is possible when each item can borrow directly from storage independently of mutable cursor state. The iterator may advance using an index while previously returned slices remain valid, so several items can coexist. B is useful when the returned view also borrows temporary state owned by the cursor or when advancing may invalidate the previous representation. Its item lifetime is tied to each mutable call, so the consumer protocol forbids retaining a view across the next call. C transfers independent ownership and permits arbitrary retention, at the cost of allocation or copying.

The choice cannot be made by counting allocations alone. Ask whether advancing invalidates prior views, whether callers need random retention, whether the backing allocation is acceptable to keep alive, and whether an owned conversion already exists at the boundary where retention begins. A lending API that every caller immediately clones may be technically correct but architecturally dishonest.

Higher-ranked callbacks offer a fourth shape. A method may create temporary scratch storage and invoke `for<'a> FnOnce(View<'a>)`, ensuring the callback works for whatever short lifetime the method supplies. That supports scoped use without exposing a cursor type. It does not let the callback return the view. Write the quantifiers in prose before syntax: “for every temporary lifetime chosen by the method, the callback can consume a view valid for that lifetime.” This phrasing prevents the common error of imagining one universally long borrow.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Does each borrow create a distinct view type? | a lifetime-indexed associated family | one fixed associated item |
| May the consumer retain the value? | owned output or explicit conversion | a lending API plus undocumented clone workaround |
| Must a callback accept every temporary lifetime? | a higher-ranked `for<'a>` bound | one function-wide lifetime coupling all calls |
| Must the component be dynamically erased? | move erasure after conversion to an owned stable type | forcing a GAT-rich trait into an unsuitable object boundary |

### A rigorous working procedure

1. Draw the owner, cursor, current borrow, and returned view as separate nodes.
2. Label each lifetime with its chooser: caller, method borrow, source owner, or higher-ranked callee.
3. State whether outputs must coexist. If yes, a single mutable lending cursor may be the wrong interface.
4. Write the GAT and required `where Self: 'a` relationship before implementing the method.
5. Add compile-fail cases for escape and overlapping iteration, plus a positive conversion to owned data.
6. Keep dynamic extension outside the lending family unless the erased contract genuinely needs it.

### Failure patterns and principled repairs

Lifetime-heavy interfaces usually fail because a family of borrowed outputs has been flattened into one lifetime or because a callback is allowed to choose less than the operation requires. Repair them by stating who selects each lifetime, which value owns the backing storage, and whether successive yielded items may coexist.

### Interpreting `for<'a>` as one very long lifetime

Read it as a caller-selected fresh lifetime for every use covered by the bound.

### Returning a lent view and calling `next` again while retaining it

Consume the view before the next exclusive borrow or convert it to owned data.

### Making every layer generic over the source lifetime

Contain borrowing in snapshot and codec boundaries; cross durable boundaries with owned values.

### Using lending only to claim zero allocations

Evaluate retention, mutation, dyn compatibility, and caller ergonomics before selecting the protocol.

### What the compiler cannot decide for you

GATs can encode that a view is valid only for the borrow that produced it. They do not prove that borrowing is faster, that retained backing storage is acceptable, or that the consumer protocol is ergonomic. Higher-ranked bounds prove capability across lifetime choices; they do not create longer-lived data.

Use lending when the product benefits from ephemeral views and sequential access. If callers routinely need to retain many items, an ordinary iterator of owned or independently borrowed items may be the more honest design.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish one associated type from a lifetime-indexed family of associated types, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime family map** and state which evidence could falsify the claim.

2. **Outcome 2.** For design a lending cursor whose returned view cannot outlive the borrow that produced it, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime family map** and state which evidence could falsify the claim.

3. **Outcome 3.** For read `for<'a>` as universal quantification chosen by the caller rather than a long concrete lifetime, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime family map** and state which evidence could falsify the claim.

4. **Outcome 4.** For identify when a bound accidentally requires a view for one specific lifetime instead of every usable borrow, construct one positive and one causal negative example. Mark the first decisive fact in the **lifetime family map** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

Treat each call to `next` as a temporary exclusive loan of the cursor. Predict which returned row may be retained and why calling `to_owned` changes the next operation’s legality.

```rust
trait LendingCursor {
    type View<'a>
    where
        Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::View<'a>>;
}

struct Lines<'input> {
    remaining: &'input str,
}

impl LendingCursor for Lines<'_> {
    type View<'a> = &'a str where Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::View<'a>> {
        if self.remaining.is_empty() {
            return None;
        }
        let (line, rest) = self.remaining
            .split_once('\n')
            .unwrap_or((self.remaining, ""));
        self.remaining = rest;
        Some(line)
    }
}
```

### Trace the example

Draw `input`, `TableCursor`, `remaining`, the method borrow, and `RowView`. On the first call, show how the view’s lifetime is tied to the mutable borrow of the cursor, even though the underlying text outlives both. Explain why the cursor may shorten the source lifetime safely but may not lengthen the method borrow.

Then write two consumers: one that prints each row immediately and one that stores rows. The first should remain allocation-free; the second must choose an ownership strategy explicitly. This comparison is the real API decision, not whether GAT syntax compiles.

### Use it in AxiomStore

AxiomStore’s `RecordCodec` exposes `type View<'a>` and decodes borrowed record views directly from archive bytes. Snapshot iteration lends those views while the snapshot remains borrowed. Key and value domain checks run directly on borrowed `&str` fields; allocation occurs only when the caller requests an owned `Record`. Runtime policy validation and durable mutation occur only after an explicit conversion into an owned `Record`. This creates a clear boundary between zero-copy inspection and retained state rather than spreading lifetimes through every layer.

For AxiomStore, maintain a lending contract:

```text
backing owner: Snapshot
cursor state: offset + remaining
borrow creator: &mut RecordCursor::next
returned family: RecordView<'borrow>
operations allowed while view lives
owned escape: RecordView::to_owned
invalid escape example
```

The codec and cursor own this relationship. Validators consume `&Record` or owned `Record` and therefore do not inherit snapshot lifetimes.

## Practice sequence

1. **Quantifier translation.** Rewrite three prose requirements using “for every” or “for one chosen” and then express them with HRTBs or ordinary lifetime parameters.
2. **Lending cursor.** Implement a row cursor whose views borrow from the cursor call. Add the compile-fail retained-view case to the documentation.
3. **Owned escape.** Add `to_owned` and measure only allocation counts, not blanket performance claims.
4. **Coexistence redesign.** Modify the requirement so two rows must coexist; compare an index-based borrowed view, an arena, and owned rows.
5. **Dyn boundary review.** Keep a dynamic validator registry alongside a static GAT codec and explain why the hybrid is clearer.

Complete the [workbook](workbook.md) and [Lending Table](../../labs/module-03-lending-table/README.md). The compiler cases must identify the lifetime chooser and backing owner for every accepted or rejected view.

## Ready to continue

Proceed when you can read `for<'a>` aloud with the correct quantifier, derive a GAT’s owner relationship, predict whether two yielded views may coexist, and redesign an API when the consumer needs retention. A correct answer must distinguish “the source lives long enough” from “the mutable cursor borrow is still active.”

## Primary Rust references

- The Rust Reference: higher-ranked trait bounds
- The Rust Reference: associated items and generic associated types
- The Rust stabilization announcement and standard-library lending-style APIs

Use the GAT and HRTB references to verify syntax and required bounds. Keep the chapter’s quantifier map beside them; syntax without chooser and owner analysis is not mastery.

## Continue

Continue to [Module 94 — Const Generics, Witness Types, and Compile-Time Invariants](../module-94-const-generics-witness-types-and-compile-time-invariants/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
