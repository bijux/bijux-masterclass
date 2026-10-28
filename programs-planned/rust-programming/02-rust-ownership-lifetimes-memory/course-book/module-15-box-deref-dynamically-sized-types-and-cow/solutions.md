# Reasoned solutions — Module 15: Box, Deref, Dynamically Sized Types, and Cow

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Box, Deref, Dynamically Sized Types, and Cow**, not to substitute for an attempt. The decisive question is: *When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-direct-recursion.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Direct recursive value size is infinite.
- **Causal explanation:** The compiler rejects the specimen because direct recursive value size is infinite.
- **Principled repair:** Place recursive edges behind `Box` or another intentional indirection so the containing value has finite size.
- **Weak repair to reject:** Do not impose an arbitrary fixed recursion depth as a type-level workaround.

### 2. `02-boxed-recursion.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Box gives recursive edges fixed size.
- **Causal explanation:** The specimen compiles because box gives recursive edges fixed size.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

### 3. `03-move-out-of-unpinned-box.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Ordinary Box does not prohibit moving its pointee out.
- **Causal explanation:** The specimen compiles because ordinary Box does not prohibit moving its pointee out.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

### 4. `04-box-array-unsizes.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A boxed array can coerce to boxed slice.
- **Causal explanation:** The specimen compiles because a boxed array can coerce to boxed slice.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

### 5. `05-question-sized.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** T: ?Sized accepts a str referent.
- **Causal explanation:** The specimen compiles because t: ?Sized accepts a str referent.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

### 6. `06-dst-field-not-last.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A dynamically sized field must be last.
- **Causal explanation:** The compiler rejects the specimen because a dynamically sized field must be last.
- **Principled repair:** Put the dynamically sized field last, or store it behind a pointer such as `Box<str>`.
- **Weak repair to reject:** Do not assume a layout the type system cannot represent.

### 7. `07-invariant-breaking-derefmut.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** DerefMut can compile while violating a domain invariant.
- **Causal explanation:** The specimen compiles because derefMut can compile while violating a domain invariant.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

### 8. `08-cow-borrowed-owned.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Cow can preserve a borrowed fast path.
- **Causal explanation:** The specimen compiles because cow can preserve a borrowed fast path.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not introduce indirection, `DerefMut`, or allocation when the demonstrated representation does not require it.

## Exercise reasoning and worked answers
1. Place `Box` only where the type refers to itself by value. Nonrecursive payloads remain inline. Indirection terminates compile-time size; it is not needed on leaves merely for symmetry.
2. Two child boxes allocate each subtree root separately and permit replacing children independently. One boxed tuple uses one allocation for both child values at that level but couples their storage and replacement. Real tree shape and mutation decide.
3. Accept `&str` for text observation, `&String` only when String-specific identity/capacity matters, and `&T` for a boxed domain value. Ownership wrapper details should not leak into ordinary read APIs.
4. Provide `new`, `as_str`, and `replace` that validates the candidate before assignment. `Deref<Target=str>` may be defensible for read-only transparency; `DerefMut<Target=String>` is not.
5. `T: ?Sized` permits both sized and unsized referents behind a reference. `size_of_val` uses runtime metadata for slices/str. The generic function itself remains sized because the reference parameter has known size.
6. `into_boxed_slice` preserves elements and fixed length while discarding the growable-capacity interface; implementations may shrink excess capacity. Do not promise a specific allocator action beyond API guarantees.
7. Check whether transformation is needed before allocating. Return `Cow::Borrowed(input)` exactly when input already satisfies the normalization contract; otherwise build `String` and return `Owned`.
8. Immediate `into_owned` clones the borrowed branch, removing the intended allocation benefit. Return `String` directly unless other callers exploit borrowing or ownership variation is semantically useful.
9. Recursive evaluation matches tree structure but can overflow on adversarial depth. Iterative postorder evaluation uses explicit stacks and has heap-bounded depth. Both borrow nodes; neither needs cloning.
10. `Box<str>` gives one exclusive fixed owner; `String` supports later mutation; `Rc<str>` gives shared ownership. Choose only after snapshot sharing requirements are stated. Module 16 can then justify or reject `Rc`.

### Post-key transfer

Redesign an expression tree and text-normalization API, showing which allocations are necessary and which are conditional.



## Laboratory comparison

The complete laboratory implementation is in [`module-05-boxed-expressions/solution`](../../labs/module-05-boxed-expressions/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Box, Deref, Dynamically Sized Types, and Cow**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.
- Explain Deref, deref coercion, method lookup, and why custom Deref is not ordinary inheritance.
- Reason about sized and dynamically sized types, fat pointers, metadata, unsizing, boxed slices, and boxed strings.
- Use Cow only when the common path can borrow and a well-defined transformation sometimes requires ownership.
- Choose among inline ownership, Box, Rc, handles, arenas, and borrowed views from topology and cost.

A complete explanation of **Box, Deref, Dynamically Sized Types, and Cow** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
