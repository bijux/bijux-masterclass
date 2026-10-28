# Laboratory 16 — Shared Ownership Graph

**Course 2 · Module 16: Rc, Weak, and Ownership Graphs**

[Chapter](../../course-book/module-16-rc-weak-and-ownership-graphs/index.md) · [Workbook](../../course-book/module-16-rc-weak-and-ownership-graphs/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Rc, Weak, and Ownership Graphs**: Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear? The product must make **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **liveness graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

## Working route

1. Read the product contract and run the starter’s baseline checks for **Shared Ownership Graph**.
2. Draw the smallest **liveness graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 16 — Shared Ownership Graph**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Shared Ownership Graph**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.
- Use Rc::clone, downgrade, upgrade, strong_count, weak_count, get_mut, and make_mut with their exact preconditions.
- Prevent strong cycles by assigning ownership direction and weak observers/backlinks deliberately.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 16 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **liveness graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
