# Laboratory 5 — Typed Workflow State Machine

This is the independent product for **Course 1, Module 5: Structs, Enums, Methods, and Pattern Matching**. Read the [module chapter](../../course-book/module-05-structs-enums-methods-and-pattern-matching/index.md) and complete its [workbook](../../course-book/module-05-structs-enums-methods-and-pattern-matching/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How can the type system make valid states representable and contradictory states difficult or impossible to construct?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

### Objective

Build an independent package whose public API makes task identity, priority, status, and legal transitions explicit. The laboratory is not a reduced capstone copy; it is a focused proof that you can turn a state graph into a private, testable model.

The complete specification is mirrored at `labs/module-05-state-machine/README.md`. Do not inspect the `solution` directory until the independent attempt passes the required behavioral tests.

### Required model

Implement:

```rust
pub struct TaskId(/* private non-zero u64 */);

pub enum Priority {
    Low,
    Normal,
    High,
}

pub enum Status {
    Todo,
    Doing,
    Done,
}

pub struct Task {
    // private fields
}
```

`Task` owns its title. Accessors expose borrowed or copied values as appropriate.

### Required invariants

1. `TaskId` cannot be constructed from zero through the public API.
2. A new task begins in `Status::Todo`.
3. The title is not empty after trimming.
4. The only legal state cycle is:

   ```text
   Todo -> Doing -> Done -> Todo
   ```

5. A rejected transition preserves every task field.
6. No public operation can assign an arbitrary status.

### Required operations

- `TaskId::new`;
- `Task::try_new` or a documented equivalent;
- `id`, `title`, `priority`, and `status` accessors;
- `rename` with validation-before-mutation;
- `start`, `complete`, and `reopen`;
- total textual rendering for `Priority` and `Status`;
- a structured title error;
- a structured transition error carrying source and target.

### Required tests

At minimum:

- zero and non-zero ID construction;
- empty, whitespace-only, valid, and boundary-length titles;
- initial status;
- complete legal cycle;
- all six illegal source-target pairs;
- exact transition error contents;
- equality of the whole task before and after every rejected operation;
- rename success and rename failure preservation;
- exhaustive stable tokens for all priority and status variants.

Do not test only `is_err()`. Compare the error and post-state.

### Analysis deliverable

Submit a table showing the representation before and after:

| Concern | Weak representation | Typed representation | Remaining runtime check |
|---|---|---|---|
| identity | raw `u64` | `TaskId` | non-zero at construction |
| state | strings/flags | `Status` | transition legality |
| title | unrestricted `String` | private owned field | content validation |
| mutation | public assignment | named methods | operation-specific policy |

Add a receiver table for every public method.

### Constraints

- standard library only;
- safe Rust only;
- no public fields;
- no general status setter;
- no panic-based user-input validation;
- no direct `.unwrap()` or `.expect()` in library code;
- no wildcard in domain rendering;
- no clone added only to bypass ownership reasoning.

### Verification

From the course root:

```bash
cargo test -p rust-foundations-lab-05
cargo clippy -p rust-foundations-lab-05 --all-targets -- -D warnings
cargo fmt --all -- --check
```

### Comparison criteria

After completion, inspect `labs/module-05-state-machine/solution/`. Compare:

- public surface;
- transition centralization;
- mutation ordering;
- error information;
- tests for preservation.

Do not replace a stronger independent design merely because the reference differs.

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

> How can the type system make valid states representable and contradictory states difficult or impossible to construct?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Typed Workflow State Machine**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
