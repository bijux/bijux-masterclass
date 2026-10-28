# Laboratory 37 — Persistent History

This is the independent product for **Course 4, Module 37: Recursive Data and Structural Sharing**. Read the [module chapter](../../course-book/module-37-recursive-data-and-structural-sharing/index.md) and complete its [workbook](../../course-book/module-37-recursive-data-and-structural-sharing/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

The executable crate is `labs/module-07-persistent-history/README.md`. The target is an immutable outline whose versions share unchanged nodes.

### Representation and identity

A node owns a title and `Vec<Rc<Node>>` children. Domain equality is value equality. `Rc::ptr_eq` is used only in tests that inspect structural sharing; it is not the definition of equal outlines.

Draw the ownership graph for a root with two children, then draw the graph after renaming path `[0]`. Mark newly allocated nodes and shared nodes. The expected update copies only the target and its ancestor spine.

### `rename_at_path`

The operation returns a new root or `PathError`. It must:

- leave the old root usable and unchanged;
- share siblings outside the changed path;
- preserve child order;
- report depth and invalid child index;
- perform no mutation through interior mutability.

Test the root path, a one-level path, a deeper path, and an invalid path. On failure, no partial version exists.

### Depth-first traversal

Provide an explicit-stack traversal for titles. Push children in reverse so output remains left-to-right. This design avoids call-stack depth as the traversal mechanism. State its auxiliary-space model in terms of tree shape.

### Transfer: insertion by path copying

Add a child to the node at a selected path. Share all existing unaffected children. Define whether the new child is appended or inserted at a position; the published solution appends. Test that the previous version has no new child and that an unchanged subtree retains pointer identity.

### Cost ledger

Do not claim persistent updates are categorically faster than cloning. Record:

- allocations proportional to changed path length;
- `Rc` clone operations for shared child handles;
- retained memory while old versions remain alive;
- traversal stack allocation;
- title cloning on rebuilt ancestors.

This is a model, not a benchmark result.

### Defects your tests must catch

- deep-cloning the entire tree;
- modifying children through `RefCell` and calling the result persistent;
- strong parent backlinks that create cycles;
- returning references into a newly created temporary version;
- comparing versions only by pointer identity;
- recursive traversal over attacker-controlled depth without a documented bound.

Submit graph diagrams, sharing assertions, value-equality assertions, invalid-path evidence, and the cost ledger. Defend why `Rc` is used for immutable shared ownership, why no `Weak` parent edge is needed in this model, and how the algorithm would change if nodes required stable globally unique identities.

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Persistent History**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
