# Reasoned Solutions — Module 16: Rc, Weak, and Ownership Graphs

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-rc-weak-graph/README.md) · [Memory Workspace guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 16: Rc, Weak, and Ownership Graphs**. Compare the reasoning against this question: *Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-rc-owner-clone.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Rc clone shares one allocation.
- **Causal explanation:** The specimen compiles because rc clone shares one allocation.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 2. `02-rc-deep-clone.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Cloning the pointee creates a distinct allocation.
- **Causal explanation:** The specimen compiles because cloning the pointee creates a distinct allocation.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 3. `03-mutate-shared-rc.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Shared Rc access cannot mutate ordinary T.
- **Causal explanation:** The compiler rejects the specimen because shared Rc access cannot mutate ordinary T.
- **Principled repair:** Require uniqueness with `Rc::get_mut`, clone-on-write with `make_mut`, or use interior mutability only when shared mutation is the contract.
- **Weak repair to reject:** Do not cast shared access into mutable access.

### 4. `04-get-mut-unique.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** get_mut succeeds while owner is unique.
- **Causal explanation:** The specimen compiles because get_mut succeeds while owner is unique.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 5. `05-make-mut-diverges.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** make_mut clones on shared mutation.
- **Causal explanation:** The specimen compiles because make_mut clones on shared mutation.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 6. `06-weak-expiration.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Weak upgrade reports liveness.
- **Causal explanation:** The specimen compiles because weak upgrade reports liveness.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 7. `07-strong-cycle-compiles.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A strong cycle can compile and leak.
- **Causal explanation:** The specimen compiles because a strong cycle can compile and leak.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

### 8. `08-value-versus-pointer-equality.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Equal values can occupy distinct allocations.
- **Causal explanation:** The specimen compiles because equal values can occupy distinct allocations.
- **Principled repair:** No repair is required. Preserve the example and state which provenance, liveness, representation, or address condition makes it valid.
- **Weak repair to reject:** Do not confuse cloning an owner with cloning its pointee, and do not turn every edge into strong ownership.

## Exercise reasoning and worked answers
1. Each `Rc::clone` adds a strong owner; downgrade adds a weak observer. Dropping the final strong owner drops `T`; later upgrades return `None`. Weak bookkeeping can remain until weak handles drop. Draw local temporaries too.
2. Use names such as `share_snapshot` for `Rc::clone` and `duplicate_snapshot` for deep value cloning. Assert `ptr_eq` for sharing and non-`ptr_eq` with equal values for duplication.
3. Children keep descendants alive; weak parents do not keep ancestors alive. After dropping the root and any external child owners, all weak probes must fail to upgrade.
4. A cycle remains upgradeable through a weak probe after external roots drop. Replacing one back edge with `Weak` allows counts to reach zero.
5. `get_mut` returns `Option<&mut T>` only under its uniqueness contract. Mutation can return a domain error or choose copy-on-write rather than panic.
6. After `make_mut` on one shared owner, values diverge and `ptr_eq` becomes false. Other aliases retain the old allocation/value.
7. Store a weak self-observer in the callback or ensure the owner does not store a callback that strongly captures it. Upgrade only during invocation.
8. `Rc` offers direct independent ownership but cycles and distributed mutation. An arena centralizes lifetime/deletion and uses explicit IDs, fitting mutable serializable graphs better.
9. `&Rc<T>` is justified only for clone/count/identity/downgrade operations. Ordinary methods should accept `&T`, allowing any owner representation.
10. Weak watchers are appropriate when observation must not preserve snapshots. Strong watchers are appropriate when registration promises retention/history. The product contract decides.

### Post-key transfer

Audit a parent/child/observer graph, choose strong and weak edges, and prove teardown and bounded retention with tests.

## Reference implementation comparison

The complete laboratory implementation is in [`module-06-rc-weak-graph/solution`](../../labs/module-06-rc-weak-graph/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Rc, Weak, and Ownership Graphs**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.
- Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions.
- Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately.
- Distinguish value equality, allocation identity, runtime handles, and liveness observations.
- Bound retained shared state through explicit eviction or retention policy instead of assuming reference counting is collection.

A complete explanation of **Rc, Weak, and Ownership Graphs** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

Build a **liveness graph**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Distinguish value equality, allocation identity, runtime handles, and liveness observations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Bound retained shared state through explicit eviction or retention policy instead of assuming reference counting is collection.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the liveness graph.

### Laboratory transfer review

For [Shared Ownership Graph](../../labs/module-06-rc-weak-graph/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Memory Workspace, Module 16 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Rc, Weak, and Ownership Graphs**, which relationship decides this question: “Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Memory Workspace?
