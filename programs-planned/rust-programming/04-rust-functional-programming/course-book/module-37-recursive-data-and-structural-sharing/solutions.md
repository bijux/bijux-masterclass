# Reasoned solutions — Module 37: Recursive Data and Structural Sharing

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Recursive Data and Structural Sharing**, not to substitute for an attempt. The decisive question is: *How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `case-01.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** recursive values need indirection at recursive positions.
- **Causal explanation:** The specimen compiles because recursive values need indirection at recursive positions.
- **Principled repair:** place indirection at the recursive edge
- **Weak repair to reject:** box every field regardless of recursion

### 2. `case-02.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a directly recursive enum has infinite size.
- **Causal explanation:** The compiler rejects the specimen because a directly recursive enum has infinite size.
- **Principled repair:** insert Box/Rc at the recursive edge based on ownership needs
- **Weak repair to reject:** add an arbitrary large array as a fake bound

### 3. `case-03.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Rc permits persistent versions to share immutable nodes.
- **Causal explanation:** The specimen compiles because rc permits persistent versions to share immutable nodes.
- **Principled repair:** use Rc when old and new versions share single-threaded immutable structure
- **Weak repair to reject:** use Arc without cross-thread ownership

### 4. `case-04.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a value cannot be moved out through shared Rc ownership.
- **Causal explanation:** The compiler rejects the specimen because a value cannot be moved out through shared Rc ownership.
- **Principled repair:** borrow the value or use Rc::try_unwrap when uniqueness is proven
- **Weak repair to reject:** clone the inner value automatically

### 5. `case-05.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** path copying creates a new ancestor while sharing unchanged children.
- **Causal explanation:** The specimen compiles because path copying creates a new ancestor while sharing unchanged children.
- **Principled repair:** clone Rc handles for unchanged subtrees
- **Weak repair to reject:** deep-clone the entire tree

### 6. `case-06.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** a returned reference cannot point into a temporary transformed value.
- **Causal explanation:** The compiler rejects the specimen because a returned reference cannot point into a temporary transformed value.
- **Principled repair:** return an owned value or borrow from caller-owned storage
- **Weak repair to reject:** leak the temporary

### 7. `case-07.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** iterative traversal can make stack state explicit.
- **Causal explanation:** The specimen compiles because iterative traversal can make stack state explicit.
- **Principled repair:** use explicit stack when recursion depth is untrusted
- **Weak repair to reject:** reverse children accidentally and change order

### 8. `case-08.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Rc does not provide mutable dereference through shared ownership.
- **Causal explanation:** The compiler rejects the specimen because rc does not provide mutable dereference through shared ownership.
- **Principled repair:** construct a new persistent version or prove uniqueness with get_mut
- **Weak repair to reject:** add RefCell without reviewing runtime borrow behavior

## Exercise reasoning

### Exercise 1 — Model recursive data

An enum variant cannot contain another `Expr` directly because its size would be infinite. `Box<Expr>` gives the recursive field a known pointer size. A `Vec<Expr>` also provides indirection because the vector header has fixed size while elements live in a separate allocation; this is useful for n-ary nodes. The choice affects ownership, allocation count, and traversal shape.

### Exercise 2 — Structural map and fold

For a literal, map returns a new literal with doubled value; count returns one. For addition, map recursively transforms both children and reconstructs addition; count returns one plus both child counts. For negation, map transforms its child; count returns one plus child count. The structure itself determines the recursion. Combining unrelated state mutation outside the function would obscure this proof.

### Exercise 3 — Trace path copying

Every ancestor from the root to the changed leaf is newly allocated so its child pointer can reference the new subtree. Siblings not on the path are shared through cloned `Rc` handles. The old root still reaches the original leaf. Allocation and traversal are O(height), while unchanged subtrees are not deep-cloned. A degenerate tree can make height O(n), so shape matters.

### Exercise 4 — Immutable interface, local mutation

When the `Rc` has one strong owner, `make_mut` can provide mutable access to the allocation without cloning. When multiple owners exist, it clones the inner value and makes the current handle unique before mutation; therefore the inner type must be cloneable for that path. The public operation can still return a new version while old shared versions remain unchanged. This is copy-on-write, not proof that mutation disappeared.

### Exercise 5 — Persistent audit ordering

The natural iterator follows head links and yields newest-first in O(1) setup. Chronological reporting can collect references into a temporary vector and reverse iteration, or recursively render older entries first if depth is safely bounded. Append remains O(1). Make ordering explicit in method names and tests; silently claiming insertion order would be false.

### Exercise 6 — Choose mutable or persistent

The single-owner accumulator usually benefits from ordinary local mutation: no consumer needs prior versions, so structural sharing adds allocations and indirection without product value. The retained history has simultaneous old and new views, making persistence meaningful. The functional design principle is not “immutable everything”; it is aligning update semantics with versioning requirements.



## Laboratory comparison

The complete laboratory implementation is in [`module-07-persistent-history/solution`](../../labs/module-07-persistent-history/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Recursive Data and Structural Sharing**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Define recursive algebraic data with the appropriate indirection.
- Implement structural map, fold, and search operations with explicit base and recursive cases.
- Use `Rc` structural sharing when immutable versions must coexist.
- Distinguish immutable public semantics from efficient local mutation of uniquely owned data.
- Recognize recursion-depth and allocation costs and select iterative alternatives when required.

A complete explanation of **Recursive Data and Structural Sharing** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
