# Reasoned solutions — Module 12: Lifetime Relationships and Borrowed APIs

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Lifetime Relationships and Borrowed APIs**, not to substitute for an attempt. The decisive question is: *What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-single-source-elision.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** One input reference determines output.
- **Causal explanation:** The specimen compiles because one input reference determines output.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add longer lifetimes or ownership merely to avoid stating the actual provenance relationship.

### 2. `02-ambiguous-output-source.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Two inputs need an explicit output relationship.
- **Causal explanation:** The compiler rejects the specimen because two inputs need an explicit output relationship.
- **Principled repair:** State which input supplies the output lifetime, or return an enum/owned result when the choice is genuinely dynamic.
- **Weak repair to reject:** Do not force unrelated inputs to share one lifetime only to satisfy elision.

### 3. `03-independent-choice-enum.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An enum can preserve independent source lifetimes.
- **Causal explanation:** The specimen compiles because an enum can preserve independent source lifetimes.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add longer lifetimes or ownership merely to avoid stating the actual provenance relationship.

### 4. `04-reference-to-local.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Annotations cannot make a local owner survive return.
- **Causal explanation:** The compiler rejects the specimen because annotations cannot make a local owner survive return.
- **Principled repair:** Return owned data or borrow storage owned by the caller.
- **Weak repair to reject:** Do not add `static`, leak the local owner, or transmute the lifetime.

### 5. `05-explicit-shortening.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An outlives bound permits a weaker returned lifetime.
- **Causal explanation:** The specimen compiles because an outlives bound permits a weaker returned lifetime.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add longer lifetimes or ownership merely to avoid stating the actual provenance relationship.

### 6. `06-temporary-dropped-too-soon.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A method borrow cannot outlive a temporary owner statement.
- **Causal explanation:** The compiler rejects the specimen because a method borrow cannot outlive a temporary owner statement.
- **Principled repair:** Bind the temporary owner to a local variable whose scope covers every use of the borrow.
- **Weak repair to reject:** Do not leak the temporary to make the borrow appear permanent.

### 7. `07-owned-type-static-bound.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** T: static does not require the local owner to live forever.
- **Causal explanation:** The specimen compiles because t: static does not require the local owner to live forever.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not add longer lifetimes or ownership merely to avoid stating the actual provenance relationship.

### 8. `08-view-outlives-owner.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A reference-bearing value cannot survive its owner.
- **Causal explanation:** The compiler rejects the specimen because a reference-bearing value cannot survive its owner.
- **Principled repair:** Keep the owner alive with the reference-bearing value, or redesign the value to own the required data.
- **Weak repair to reject:** Do not detach the reference with an unsafe lifetime cast.

## Exercise reasoning and worked answers
### 1. Expand elision

Each input reference receives a distinct lifetime. With one input reference, outputs use that lifetime. In a method, elided outputs use the receiver lifetime. An opaque iterator borrowing `self` normally needs `+ '_` when the capture is not otherwise visible.

### 2. Source identification

A correct answer names a field or input owner, not merely “the parameter.” If a branch can return either input, the output must be valid for a common lifetime or be represented by an enum preserving distinct sources.

### 3. Independent lifetimes

`Diff<'left, 'right>` avoids coupling. A method `fn left_only(&self) -> &'left str` may need to consume or explicitly return the stored field; an accessor through `&self` normally returns for the shorter receiver borrow. An `into_left(self) -> &'left str` expresses the original lifetime cleanly.

### 4. Consuming a view

`fn text(&self) -> &str` returns a reference limited by the borrow of the view. `fn into_text(self) -> &'doc str` consumes the view and returns the stored reference for its declared source lifetime.

### 5. `'static` classification

A literal can produce `&'static str`. An owned `String` value usually satisfies `T: 'static` because it contains no borrowed data, but `&String` is not automatically `'static`. A leaked box can produce a `'static` reference by intentionally forfeiting reclamation. A closure capturing a local reference is not `'static`; one moving owned data may be.

### 6. Mutable reference slot

The accepted value must be `&'a T` for a slot of type `&'a T`. Otherwise a short reference could be written and later read as though valid for `'a`.

### 7. Temporary scope rewrite

Explicit bindings make destruction points visible and robust against refactoring. Some `let` borrows already receive lifetime extension; function arguments generally live through the statement. The rewrite should not claim universal extension.

### 8. Borrowed versus ID

A reference proves immediate validity and prevents invalidating mutation. An ID releases the borrow, does not keep the target alive, and requires fallible lookup. The correct choice follows the caller's temporal needs.

### 9. Zero-copy token enum

Every borrowing variant carries `'src`. An owned conversion allocates only for borrowed variants, producing an enum with `String` fields and no source lifetime.

### 10. Lifetime minimization

Remove names used only once in inputs and no outputs; elision can handle them. Remove outlives bounds already implied by field types or not justified by a returned/stored relationship. Precision means fewer accidental constraints, not more annotations.

### Post-key transfer

Repair a parser whose single lifetime unnecessarily couples source input to scratch state, then decide which results should borrow and which should own.



## Laboratory comparison

The complete laboratory implementation is in [`module-02-zero-copy-records/solution`](../../labs/module-02-zero-copy-records/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Lifetime Relationships and Borrowed APIs**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Derive elision and explicit relationships for one-source and multiple-source APIs.
- Use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance.
- Design structs and enums containing references while accounting for temporary and drop scopes.
- Reject unnecessary lifetime coupling and choose owned output when retention must outlive input borrowing.

A complete explanation of **Lifetime Relationships and Borrowed APIs** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
