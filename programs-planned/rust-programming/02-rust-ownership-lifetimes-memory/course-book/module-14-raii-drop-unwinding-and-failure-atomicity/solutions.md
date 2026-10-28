# Reasoned solutions — Module 14: RAII, Drop, Unwinding, and Failure Atomicity

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md)

Use these explanations to review your reasoning about **RAII, Drop, Unwinding, and Failure Atomicity**, not to substitute for an attempt. The decisive question is: *Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-direct-drop-call.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Drop::drop cannot be called directly.
- **Causal explanation:** The compiler rejects the specimen because drop::drop cannot be called directly.
- **Principled repair:** Use `drop(value)` to consume the value and run its destructor at the chosen point.
- **Weak repair to reject:** Do not call `Drop::drop` directly or duplicate cleanup logic manually.

### 2. `02-move-field-from-drop-type.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A field cannot be moved out of a Drop type directly.
- **Causal explanation:** The compiler rejects the specimen because a field cannot be moved out of a Drop type directly.
- **Principled repair:** Represent the movable field as `Option<T>` and use `take`, or use a consuming transition that leaves a valid drop state.
- **Weak repair to reject:** Do not clone the field or bypass the destructor with unchecked moves.

### 3. `03-option-take-transition.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Option::take leaves a valid represented state.
- **Causal explanation:** The specimen compiles because option::take leaves a valid represented state.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

### 4. `04-field-drop-order.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A trace can observe deterministic field order.
- **Causal explanation:** The specimen compiles because a trace can observe deterministic field order.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

### 5. `05-explicit-drop-releases-guard.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Dropping a guard ends its mutable borrow.
- **Causal explanation:** The specimen compiles because dropping a guard ends its mutable borrow.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

### 6. `06-consuming-commit.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Commit consumes the session.
- **Causal explanation:** The specimen compiles because commit consumes the session.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

### 7. `07-panicking-destructor-compiles.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** The compiler permits but design review rejects panicking Drop.
- **Causal explanation:** The specimen compiles because the compiler permits but design review rejects panicking Drop.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

### 8. `08-forgotten-guard-compiles.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Safe leaks can skip cleanup.
- **Causal explanation:** The specimen compiles because safe leaks can skip cleanup.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not duplicate cleanup manually or make destructors responsible for recoverable business decisions.

## Exercise reasoning and worked answers
### 1. Destruction trace

Locals generally drop in reverse declaration order at their drop-scope exit. A struct's own destructor runs before its fields, and fields then drop in declaration order. Tuple elements and array elements drop in element order. Shadowed bindings remain separate values; do not assume the old one drops at the shadowing line. Explicit trace output is the evidence, but correctness should not depend on unspecified standard-collection element order.

### 2. Narrow guard

Move the flag into a separate field/component and construct `FlagGuard { flag: &mut workspace.editing }`. The rest of the workspace can be borrowed through disjoint fields where the compiler can prove separation. If methods require `&mut Workspace`, the receiver design still reunifies authority and should be split.

### 3. Field extraction

Store `buffer: Option<String>`. A consuming method takes `mut self`, calls `self.buffer.take()`, and returns the string. `Drop` processes only `Some`. The `None` state is explicit and prevents a second action. A fake empty `String` is weaker if empty is meaningful data.

### 4. Pool lease

The lease holds `item: Option<T>` and `return_to: &'a mut Vec<T>`. `Drop` pushes the item back when present. `discard(mut self)` takes and drops the item, leaving `None`; `replace(mut self, next)` takes the old item, pushes `next`, and returns old if required. Consuming methods make repeated transitions impossible.

### 5. Strong edit guarantee

The working copy is independent. The target is borrowed but not changed by the closure. If the closure panics, the working `String` drops and the target remains original. Commit validates then swaps/takes the working copy. This is a strong in-memory guarantee, not persistence crash safety.

### 6. Basic guarantee

An element-by-element transformation may leave already processed elements changed. It is panic-safe at the basic level if the collection remains valid and all elements satisfy type invariants. Document partial application and avoid temporarily invalid element states around callbacks.

### 7. Fallible finish

`finish` performs flush/sync/commit and returns the result. `Drop` closes local resources or discards staged output without reporting. A caller relying on drop cannot know whether data reached the intended durable destination.

### 8. Leak review

Forgetting a lease prevents its destructor, so the item is not returned and the mutable borrow is considered consumed with the forgotten value. The pool may be inaccessible for the rest of the borrow's theoretical scope or lose capacity logically. This is permitted safe behavior; an unsafe invariant cannot require all leases to drop.

### 9. Double panic audit

Potential sources include `unwrap`, `expect`, out-of-bounds indexing, `assert!`, user formatting implementations, allocation failure behavior, user callbacks, and poisoned assumptions. Destructors should use checked branches and local operations whose failure cannot be reported. Diagnostics should be best-effort outside the critical cleanup path.

### 10. Capstone session

Handle/revision sessions permit the workspace borrow to end after session creation and allow unrelated operations. They require owned staged data and conflict validation. Leaking such a session loses only its working copy and does not freeze the workspace. This topology is therefore preferable for the capstone's multi-document workflow.

### Post-key transfer

Review a boolean transaction guard, redesign it as an ownership protocol, and specify its exact unwind and explicit-finish guarantees.



## Laboratory comparison

The complete laboratory implementation is in [`module-04-resource-pool/solution`](../../labs/module-04-resource-pool/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **RAII, Drop, Unwinding, and Failure Atomicity**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Derive local, field, tuple, temporary, and scope destruction order from documented rules.
- Design RAII guards whose ownership encodes exactly one cleanup or release obligation.
- Use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states.
- Distinguish no-throw, basic, and strong in-memory failure guarantees from crash durability.
- State when destructors may not run or cannot report failure, including abort, process exit, leaks, and power loss.

A complete explanation of **RAII, Drop, Unwinding, and Failure Atomicity** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
