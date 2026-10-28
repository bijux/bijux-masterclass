# Workbook — Module 11: Places, Move Paths, and Advanced Borrowing

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Places, Move Paths, and Advanced Borrowing** without relying on surface syntax. Keep the module question in view: *Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Places, Move Paths, and Advanced Borrowing** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-disjoint-fields.rs`](../../compiler-labs/module-01/01-disjoint-fields.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-indexed-exclusive-borrows.rs`](../../compiler-labs/module-01/02-indexed-exclusive-borrows.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-split-at-mut-proof.rs`](../../compiler-labs/module-01/03-split-at-mut-proof.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-partial-move-whole-use.rs`](../../compiler-labs/module-01/04-partial-move-whole-use.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-reborrow-exclusive.rs`](../../compiler-labs/module-01/05-reborrow-exclusive.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-two-phase-method-borrow.rs`](../../compiler-labs/module-01/06-two-phase-method-borrow.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-shared-loan-still-used.rs`](../../compiler-labs/module-01/07-shared-loan-still-used.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-separate-read-and-write-phases.rs`](../../compiler-labs/module-01/08-separate-read-and-write-phases.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A payment prototype stores accounts in a vector. Its transfer method was made to compile by cloning both accounts, mutating the clones, then writing them back.

```rust
fn transfer(
    accounts: &mut Vec<Account>,
    from: usize,
    to: usize,
    amount: u64,
) -> Result<(), TransferError> {
    let mut source = accounts.get(from).cloned().ok_or(TransferError::MissingSource)?;
    let mut target = accounts.get(to).cloned().ok_or(TransferError::MissingTarget)?;

    if source.balance < amount {
        return Err(TransferError::InsufficientFunds);
    }

    source.balance -= amount;
    target.balance += amount;
    accounts[from] = source;
    accounts[to] = target;
    Ok(())
}
```

### Defects

1. `from == to` creates two clones of one account and the final assignment silently chooses one result.
2. Account metadata and audit history are duplicated even though only balances change.
3. Writing source before target would risk partial state if later code became fallible.
4. The signature takes `&mut Vec<Account>` although resizing is not required.
5. Bounds checks and transfer invariants are mixed with mutation.
6. Clone cost grows with the account structure.

### Required repair

Implement:

```rust
fn transfer(
    accounts: &mut [Account],
    from: usize,
    to: usize,
    amount: u64,
) -> Result<TransferReceipt, TransferError>
```

The repair must:

- reject equal indices;
- reject zero amounts;
- validate both indices and funds before mutation;
- use checked arithmetic for the target balance;
- acquire two disjoint mutable references through a safe split helper;
- preserve total balance;
- return an owned receipt after releasing the borrows;
- contain no account clone.

### Proof obligations

Tests must cover reversed indices, equal indices, missing source, missing target, insufficient funds, overflow, and success. Add a property-style loop over small balances asserting that successful transfers preserve the sum.

### Design defense

Explain why `Rc<RefCell<Account>>` would compile but be a worse topology for this product. The vector already owns every account, transfer is synchronous, and disjoint exclusive access is available. Shared lifetime and runtime borrow checking would add cost and new failure modes without satisfying a real requirement.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


Complete these before the independent lab.

### 1. Place classification

For each expression below, classify the base place, projections, and operation: copy, move, shared borrow, mutable borrow, or assignment.

```rust
record.count
record.title
&record.title
&mut records[2].count
*handle
pair.1 = String::from("new")
```

### 2. Partial move repair

A function must return a record's owned payload and numeric ID. Refactor without cloning and explain whether the original struct remains usable.

### 3. `Drop` extraction

Create a `Packet` type implementing `Drop` and containing `payload: Option<Vec<u8>>`. Implement `take_payload` safely. Explain why a direct field move is rejected.

### 4. Two mutable elements

Implement `two_mut<T>(&mut [T], usize, usize)` preserving argument order. Test every pair for a five-element array, including equal and invalid indices.

### 5. Borrow shortening

Refactor a function that stores `let selected = &items[index]`, logs it after a mutation, and therefore fails. Preserve the final log semantics with the narrowest allocation or copy.

### 6. Split `self`

Given `Engine { queue, completed, metrics }`, refactor `process_next(&mut self)` so it moves one job from queue to completed and updates metrics without a helper that takes all of `&mut self` while a field is borrowed.

### 7. Read–validate–write phases

Implement inventory movement between bins. All expected errors must be discovered before any quantity changes.

### 8. Reborrow trace

Write a function receiving `&mut String`, pass it through three helpers, and annotate where each reborrow starts and ends.

### 9. Receiver audit

Review six supplied method signatures and replace whole-object `&mut self` receivers with field-level functions or owned-return phases where appropriate.

### 10. Clone audit

Take a small clone-heavy program and classify each clone as required duplication, snapshot, counted-handle clone, or workaround. Remove every workaround clone.



## Part 4 — Independent laboratory



Implement the package in `labs/module-01-borrow-surgery/starter` without reading the solution.

### Product

A small portfolio holds positions in an ordered slice. The library must rebalance quantity between two distinct positions while preserving total quantity and all unrelated metadata.

### Public surface

```rust
pub struct Position { /* private */ }
pub struct RebalanceReceipt { /* private */ }
pub enum RebalanceError { /* ... */ }

pub fn rebalance(
    positions: &mut [Position],
    from: usize,
    to: usize,
    quantity: u64,
) -> Result<RebalanceReceipt, RebalanceError>;
```

Constructors and read-only accessors are required for testing.

### Contract

- indices must be distinct and in range;
- quantity must be nonzero;
- source must contain enough quantity;
- target addition must not overflow;
- every expected failure leaves every position unchanged;
- success changes only the two quantities;
- total quantity is preserved;
- returned receipt owns the symbols and resulting quantities needed after borrows end;
- no `Position` clone is permitted;
- the function accepts a slice, not a vector.

### Required technique

Use a safe helper that obtains two disjoint mutable references with `split_at_mut`. Validation must occur before mutation.

### Laboratory: Tests

At minimum:

- forward and reverse index order;
- same index;
- source and target out of range independently;
- zero quantity;
- insufficient source;
- target overflow;
- preservation after every error;
- total preservation over a matrix of small values;
- metadata unchanged.

### Design note
Submit a place/loan trace and explain why neither cloning nor `Rc<RefCell<Position>>` is justified.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-01-borrow-surgery](../../labs/module-01-borrow-surgery/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.
- Sequence validation and mutation so failure does not expose prohibited partial state.
- Repair ownership conflicts by changing topology or phases before considering Clone, RefCell, or unsafe code.


The first `memory-workspace` increment builds its internal arena.

### Why not return vector indices

A raw index can become stale after removal and slot reuse. If document 2 is removed and a new document occupies slot 2, an old index silently identifies the wrong document.

Use a `DocumentId` containing:

- slot index;
- generation counter.

Each slot stores its current generation and an optional document. Removal increments the generation before the slot becomes reusable. `get` and `get_mut` compare both components.

### Required API

```rust
pub struct DocumentId { /* private */ }

impl Workspace {
    pub fn insert(&mut self, title: String, body: String) -> Result<DocumentId, WorkspaceError>;
    pub fn get(&self, id: DocumentId) -> Option<DocumentView<'_>>;
    pub fn remove(&mut self, id: DocumentId) -> Result<(), WorkspaceError>;
}
```

`DocumentView` is introduced fully on Day 2; a temporary internal borrow may be used today.

### Borrow proof

Arena removal must not hold a mutable reference to a slot while also mutating the free-list field through a whole-object method. Split the operation into field borrows or sequence it:

1. validate ID through shared access;
2. take the value from the slot through a narrow mutable borrow;
3. update generation;
4. release the slot borrow;
5. push the index to the free list.

### Capstone: Tests

- first insertion uses a valid ID;
- removal makes the ID stale;
- slot reuse produces a different generation;
- stale `get`, `get_mut`, and `remove` fail;
- unrelated documents remain accessible;
- free-list reuse does not duplicate a live slot.

Do not expose slots or generation mutation publicly. The handle is proof-carrying identity, not direct access.



### Capstone defense

Diagnose a composite-store transfer whose lookup and mutation overlap, then derive a failure-atomic split-borrow implementation.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Use reborrowing, non-lexical lifetime shortening, two-phase borrowing, and split APIs without relying on folklore.
- Sequence validation and mutation so failure does not expose prohibited partial state.
- Repair ownership conflicts by changing topology or phases before considering Clone, RefCell, or unsafe code.

### Closed-book checkpoint

Answer closed-book.

1. What is a place expression, and why does it improve borrow reasoning?
2. Why can named fields be mutably borrowed together while two indexed elements often cannot?
3. What remains usable after a partial move?
4. Why can a field not be moved directly out of a type implementing `Drop`?
5. What is a reborrow?
6. What event usually ends an NLL borrow?
7. What is the practical role of `split_at_mut`?
8. Why should expected failures be validated before acquiring mutation borrows?
9. How can a helper taking `&mut self` cause a conflict even when it touches another field?
10. Name four structural repairs to try before cloning.
11. Why is `Rc<RefCell<T>>` not a general solution to two-element mutation?
12. How do generations prevent stale indices from silently identifying new values?

Practical check: implement `two_mut` and the rebalance core from memory in 35 minutes, including equal-index and out-of-range behavior.

### Transfer defense

Diagnose a composite-store transfer whose lookup and mutation overlap, then derive a failure-atomic split-borrow implementation.

Your answer must include:

Answer without compiling, then verify.

1. What is the base place in `seats[from].token`?
2. Why may two named fields of one struct be borrowed separately while two runtime indices may not?
3. What does `split_at_mut(k)` prove?
4. Why is `Option::take` preferable to cloning a uniquely owned token?
5. What path remains initialized after `take`?
6. Why can a type implementing `Drop` not usually have a field moved directly out?
7. When can a loan end before its lexical block?
8. What is a reborrow?
9. Why might `for item in &mut items` prevent `items.push(...)`?
10. What is wrong with mutating source before checking target overflow?
11. How can a method receiver borrow be shorter than the method body?
12. When is copying a small field a principled borrow repair?
13. What proof does a successful compilation not provide about failure atomicity?
14. How do partial initialization rules interact with branches?
15. What ownership fact must justify every clone?

#### Answer notes

1. `seats`, projected by `[from]` then `.token`. 2. Field disjointness is structural; runtime indices may be equal. 3. Its two returned slices do not overlap. 4. The token has one semantic owner and should move. 5. The `Option` remains initialized as `None`. 6. Its destructor expects a complete value. 7. After last use under non-lexical lifetime analysis. 8. A new, usually shorter borrow through an existing reference. 9. The iterator holds a mutable collection borrow and push may reallocate. 10. A later failure leaves partial state. 11. Internal reborrows can end at last use. 12. When only that copyable fact is needed, not the object identity. 13. It does not prove domain invariants or transaction order. 14. Every used path must be definitely initialized on all reaching branches. 15. The product needs two independent owned values.

#### Transfer task

Implement a bidirectional inventory transfer over a slice. Add quantity overflow checks, equal-bin rejection, and an audit record prepared before writes. Submit the place/loan table before code.
