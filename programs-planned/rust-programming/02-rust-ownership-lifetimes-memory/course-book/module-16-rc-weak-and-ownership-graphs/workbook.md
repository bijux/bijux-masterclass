# Workbook — Module 16: Rc, Weak, and Ownership Graphs

[Chapter](index.md) · [Laboratory](../../labs/module-06-rc-weak-graph/README.md) · [Memory Workspace guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Rc, Weak, and Ownership Graphs** has become a usable model rather than remembered vocabulary. Its governing question is: *Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?* Preserve your first prediction and record decisive facts in a **liveness graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 15 — Box, Deref, Dynamically Sized Types, and Cow that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?**
3. Draw the smallest **liveness graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Rc, Weak, and Ownership Graphs** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-rc-owner-clone.rs`](../../compiler-labs/module-06/01-rc-owner-clone.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-rc-deep-clone.rs`](../../compiler-labs/module-06/02-rc-deep-clone.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-mutate-shared-rc.rs`](../../compiler-labs/module-06/03-mutate-shared-rc.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-get-mut-unique.rs`](../../compiler-labs/module-06/04-get-mut-unique.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-make-mut-diverges.rs`](../../compiler-labs/module-06/05-make-mut-diverges.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-weak-expiration.rs`](../../compiler-labs/module-06/06-weak-expiration.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-strong-cycle-compiles.rs`](../../compiler-labs/module-06/07-strong-cycle-compiles.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-value-versus-pointer-equality.rs`](../../compiler-labs/module-06/08-value-versus-pointer-equality.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair

A mutable graph stores every node as `Rc<RefCell<Node>>`. Parent and child fields are all strong. Public functions clone wrappers freely, hold mutable borrow guards across callbacks, compare node addresses as IDs, and use strong counts as deletion criteria.

### Diseases

- cycles leak the graph;
- mutation conflicts panic at runtime;
- identity depends on allocation;
- strong counts change with temporary implementation details;
- callbacks can reenter while a borrow guard is active;
- every edge extends liveness whether intended or not.

### Repair alternatives

For a tree: strong children, weak parent, narrow mutation methods, explicit node IDs if needed.

For an arbitrary editable graph: central arena with generational handles and adjacency IDs.

For immutable shared DAG: `Rc<Node>` with construction-time ownership and no `RefCell`.

### Required output

Refactor one chosen product model, draw ownership and observation graphs, write a weak-probe reclamation test, and explain every remaining strong edge. Module 17 may add interior mutability only after this topology is stable.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

1. Trace strong/weak counts and destruction through a sequence of clones, downgrades, drops, and upgrades.
2. Distinguish owner clone from deep clone in API names and tests.
3. Build a tree with strong children and weak parents; prove the entire tree reclaims after root drop.
4. Construct a two-node strong cycle and detect the leak with weak probes, then repair one edge.
5. Use `Rc::get_mut` before and after creating an alias; handle `None` without panic.
6. Demonstrate `Rc::make_mut` divergence and test both value and allocation identity.
7. Find a closure-capture cycle and break it with `Weak`.
8. Compare `Rc` graph and generational arena designs for deletion, serialization, and mutation.
9. Review every function taking `&Rc<T>` and weaken it to `&T` where wrapper operations are absent.
10. Select strong or weak snapshot watchers in the capstone and defend liveness behavior.

### Interleaved reasoning pass

1. For **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the liveness graph.
2. For **Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the liveness graph.
3. For **Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the liveness graph.
4. For **Distinguish value equality, allocation identity, runtime handles, and liveness observations**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the liveness graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Rc, Weak, and Ownership Graphs** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build an immutable/shared project tree with strong child ownership, weak parent backlinks, and weak external observers.

```text
labs/module-06-rc-weak-graph/
├── starter/
└── solution/
```

### Required behavior

- construct nodes through an API that establishes parent links;
- children are strongly owned;
- parent links are weak;
- node labels are immutable after connection;
- lookup can return a cloned `Rc<Node>` when independent retention is required;
- read-only helpers accept `&Node` where possible;
- `path_to_root` handles absent parents;
- weak probes prove reclamation;
- no strong cycle exists, including through callbacks or observer storage.

### Identity

Give each node an explicit `NodeId`. Structural value equality and allocation identity must not substitute for the ID. Tests should use `Rc::ptr_eq` only to prove sharing behavior.

### Acceptance

```bash
cargo test -p rust-olm-lab-06-rc-weak-graph --all-targets
cargo clippy -p rust-olm-lab-06-rc-weak-graph --all-targets -- -D warnings
```

### Graph protocol

Construction must be centralized. A node cannot safely expose a public `children: RefCell<Vec<Rc<Node>>>` and still claim that parent links are maintained. Provide an operation that creates or attaches a child and updates both edges as one logical transaction. If the API permits reparenting, specify what happens when validation fails and prove that neither old nor new topology is left half-mutated. A simpler acceptable design makes attachment one-time and rejects a node that already has a live parent.

Choose the strong-edge direction from the liveness policy: retaining a root retains descendants; retaining a descendant does not retain ancestors. Parent backlinks and external observers therefore use `Weak<Node>`. Explain why a weak count is not ownership and why `upgrade` must be handled as a fallible liveness query rather than unwrapped.

### Required tests

Test more than tree traversal:

1. a root remains alive while any independent strong root handle exists;
2. dropping the last root reclaims descendants even while weak probes remain;
3. a retained child observes an absent parent after ancestor reclamation;
4. `path_to_root` returns stable explicit IDs and labels in the documented order;
5. a search result cloned as `Rc<Node>` intentionally prolongs that node's life;
6. no helper clones an `Rc` merely to borrow node data;
7. strong and weak counts are used only as diagnostic evidence, not product logic.

Include one deliberately cyclic alternative in the written analysis. Draw its strong-edge cycle and predict which allocations survive after external roots are dropped. Do not place the leak in the submitted implementation.

### Ownership-graph defense

Submit a table with one row per stored edge: source, target, pointer type, whether it contributes to liveness, and the product rule it encodes. The lab is incomplete if `Rc` was selected only because ordinary references were difficult. Shared ownership must correspond to an independently retainable node or root.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-06-rc-weak-graph](../../labs/module-06-rc-weak-graph/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Shared Ownership Graph**, record:

- the public behavior that demonstrates **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.
- Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions.
- Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately.
- Distinguish value equality, allocation identity, runtime handles, and liveness observations.
- Bound retained shared state through explicit eviction or retention policy instead of assuming reference counting is collection.

Change `DocumentSnapshot` retention from independent deep copies to explicit shared ownership where appropriate.

### Snapshot store

The workspace may cache `Rc<DocumentSnapshot>` by `(DocumentHandle, revision)`. Consumers receive `Rc` clones and can retain immutable history independently. A new revision creates a new snapshot; it does not mutate an existing shared snapshot.

### Watchers

A `SnapshotWatcher` holds `Weak<DocumentSnapshot>`. It can report whether the observed snapshot remains retained elsewhere. Its weak edge must not make cache eviction ineffective.

### Required distinctions

- domain identity: document handle plus revision;
- value equality: title/text contents;
- allocation identity: used only in sharing tests;
- cache ownership: strong while cached;
- watcher observation: weak.

### Reclamation tests

Remove the cache entry and drop all returned strong owners. A weak watcher must then expire. No callback stored in the snapshot may strongly capture the snapshot/cache.

Do not wrap live documents in `Rc<RefCell<_>>`; their centralized generational storage remains the mutation authority.

### Capstone defense

Audit a parent/child/observer graph, choose strong and weak edges, and prove teardown and bounded retention with tests.

### Capstone invariant trace

For the Module 16 Memory Workspace increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 16: Rc, Weak, and Ownership Graphs**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

1. Draw strong and weak edges for an unseen graph.
2. Predict when the pointee and allocation bookkeeping are destroyed.
3. Distinguish `Rc::clone` from deep cloning.
4. Explain why `Rc` does not itself permit mutation.
5. Repair a parent/child cycle.
6. Handle `Weak::upgrade` expiration as normal state.
7. Use `get_mut` and `make_mut` with correct semantic differences.
8. Separate value equality, domain identity, and pointer identity.
9. Choose arena handles instead of `Rc<RefCell>` for an arbitrary mutable graph.
10. Prove capstone snapshot reclamation with weak evidence.

### Transfer defense

Transfer **Module 16: Rc, Weak, and Ownership Graphs** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 16: Rc, Weak, and Ownership Graphs** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


1. What event drops an `Rc` payload?
2. What remains while weak references exist?
3. What does `Weak::upgrade` mean?
4. Why can an `Rc` cycle leak safely?
5. Which tree edge is normally weak and why?
6. When should an observer intentionally hold `Rc`?
7. Why are exact strong-count tests fragile?
8. What does `Rc::ptr_eq` prove?
9. What does `Rc::new_cyclic` provide?
10. Why can upgrade fail inside its construction closure?
11. What risks does `Rc<RefCell<T>>` combine?
12. How do handles avoid cycles?
13. What does cache eviction do to other owners?
14. Why is `Arc` not a mutation mechanism?
15. How do you prove reclamation semantically?

#### Answer notes

Payload drops at zero strong count; weak values can remain but cannot upgrade. Cycles retain strong counts. Weak edges encode non-owning navigation. Pointer equality proves allocation identity within the process, not semantic equality. `new_cyclic` supplies a weak handle before strong completion. `Rc<RefCell<_>>` combines shared liveness, dynamic borrowing, allocation, and cycles. Prove reclamation with an external `Weak` after dropping roots.

#### Transfer task

Model a dependency DAG with one central owner and handles, then model the same liveness with `Rc`. Compare deletion, cycle prevention, serialization, and mutation evidence.

### Closed-book defense

In five minutes, answer “Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?” using the **liveness graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Memory Workspace. A list of APIs without the deciding relationship is incomplete.
