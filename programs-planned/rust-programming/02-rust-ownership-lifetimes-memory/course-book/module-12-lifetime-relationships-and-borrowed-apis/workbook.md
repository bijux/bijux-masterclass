# Workbook — Module 12: Lifetime Relationships and Borrowed APIs

[Return to the chapter](index.md) · [Open the Memory Workspace engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Lifetime Relationships and Borrowed APIs** without relying on surface syntax. Keep the module question in view: *What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Lifetime Relationships and Borrowed APIs** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-single-source-elision.rs`](../../compiler-labs/module-02/01-single-source-elision.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-ambiguous-output-source.rs`](../../compiler-labs/module-02/02-ambiguous-output-source.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-independent-choice-enum.rs`](../../compiler-labs/module-02/03-independent-choice-enum.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-reference-to-local.rs`](../../compiler-labs/module-02/04-reference-to-local.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-explicit-shortening.rs`](../../compiler-labs/module-02/05-explicit-shortening.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-temporary-dropped-too-soon.rs`](../../compiler-labs/module-02/06-temporary-dropped-too-soon.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-owned-type-static-bound.rs`](../../compiler-labs/module-02/07-owned-type-static-bound.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-view-outlives-owner.rs`](../../compiler-labs/module-02/08-view-outlives-owner.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair


A parser stores source text, a schema label, and diagnostics:

```rust
struct ParsedRecord<'a> {
    source: &'a str,
    schema: &'a str,
    key: &'a str,
    value: &'a str,
}
```

The `key` and `value` borrow from `source`; `schema` comes from an independent registry. A method attempts to replace the schema label while retaining the source fields, but the single lifetime couples every field.

### Required analysis

Draw two owners and identify which fields borrow each. Explain why one lifetime is a lossy model even though many constructors compile by shortening both inputs to a common region.

### Repair A: independent lifetimes

Design:

```rust
struct ParsedRecord<'source, 'schema> {
    source: &'source str,
    schema: &'schema str,
    key: &'source str,
    value: &'source str,
}
```

Implement accessors and a method that consumes the record and returns one with a replacement schema of a different lifetime while preserving source slices.

### Repair B: owned schema

Evaluate storing `schema: String` or `Rc<str>` instead. State when each is stronger than a second lifetime: long storage, independent schema updates, shared registry labels, or crossing an owner boundary.

### Failure case

The original parser also tries to return `ParsedRecord` containing slices of a local normalized `String`. Repairing lifetime names cannot make that valid. Choose one:

- make normalization happen in the caller-owned source;
- return an owned parsed record;
- use `Cow` so unchanged input is borrowed and normalized input is owned;
- return offsets into an owned buffer stored separately.

### Proof

Tests must show that a short-lived schema can be attached to a long-lived source for a short scope, and that the source slices remain valid after replacing the schema within their allowed region.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:


### 1. Expand elision

Expand lifetime parameters for ten supplied functions, including methods with additional reference parameters and iterator returns.

### 2. Source identification

For five proposed signatures, state exactly which input owns the output data. Reject any signature whose implementation could return from multiple sources without expressing that fact.

### 3. Independent lifetimes

Refactor a `Diff<'a>` containing left and right text from unrelated owners into `Diff<'left, 'right>`. Add a method that returns the left-only portion with `'left`.

### 4. Consuming a view

Implement a view accessor returning a short receiver-bound reference and an `into_*` method returning the stored original-lifetime reference. Explain the difference.

### 5. `'static` classification

Classify string literals, owned strings, leaked boxes, closures capturing references, and closures capturing owned values under `&'static T` and `T: 'static`.

### 6. Mutable reference slot

Implement a slot that can be updated only with a reference satisfying the stored lifetime. Explain why accepting any shorter reference would be unsound.

### 7. Temporary scope rewrite

Rewrite six expressions that borrow temporaries into explicit owner bindings. State whether behavior changes or only clarity.

### 8. Borrowed versus ID

Design two APIs for selecting a record: one returning `&Record`, one returning `RecordId`. Compare liveness, mutation, storage, and failure behavior.

### 9. Zero-copy token enum

Implement tokens borrowing from source text and prove that no token can outlive the source. Add an owned conversion.

### 10. Lifetime minimization

A supplied API has four lifetime parameters and three outlives bounds. Remove every redundant relationship and defend the remaining ones.



## Part 4 — Independent laboratory



Implement `labs/module-02-zero-copy-records/starter`.

### Product

Parse a line-oriented metadata block without allocating key or value strings when input is already valid.

Input:

```text
name: Ada
language: Rust
role: systems engineer
```

### Public types

```rust
pub struct Field<'source> { /* key/value slices */ }
pub struct Record<'source> { /* source plus fields */ }
pub enum ParseError { /* line, reason */ }
```

### Contract

- the record and every field borrow from caller-owned source;
- blank lines are ignored;
- keys and values are trimmed by slicing, not allocation;
- empty keys are rejected with one-based line number;
- duplicate keys are rejected;
- `get` returns a value tied to the record/source;
- `into_fields` may consume the record while preserving source-lifetime slices;
- `to_owned` produces an independent owned representation;
- no reference may derive from a local normalized buffer.

### Required lifetime work

Implement at least one method where receiver elision is sufficient and one consuming method returning `'source`. Document the difference.

### Adversarial tests

- source dropped before attempted record use must be a compile-fail example in docs;
- Unicode input;
- leading/trailing whitespace;
- duplicate after trimming;
- empty and whitespace-only lines;
- owned conversion remains usable after source destruction.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-02-zero-copy-records](../../labs/module-02-zero-copy-records/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

### Outcomes mapped

- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Derive elision and explicit relationships for one-source and multiple-source APIs.
- Use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance.
- Design structs and enums containing references while accounting for temporary and drop scopes.
- Reject unnecessary lifetime coupling and choose owned output when retention must outlive input borrowing.


Add `DocumentView<'workspace>` to `memory-workspace`.

### View contract

A view contains:

- `DocumentId` by value;
- `&'workspace Document` internally;
- accessors returning title and body slices;
- line access returning a slice into the body;
- no public constructor.

Only `Workspace::get` may create a valid view after checking the generation.

### Signature derivation

```rust
pub fn get(&self, id: DocumentId) -> Option<DocumentView<'_>>
```

Expand this in the lifetime ledger. The view borrows from the receiver, not the ID. The ID is copied and has no validity role.

### Avoid self-reference

The line index stores `Range<usize>` values, not `&str` slices into the body. A view applies ranges to the current body while it holds a shared borrow. This avoids a document struct that owns a `String` and stores references into itself.

### Tests

- valid ID yields the expected title/body;
- stale ID yields `None`;
- line slices are borrowed and exact;
- a view prevents mutation in a rustdoc `compile_fail` case;
- dropping the view permits later mutation;
- no title/body clone occurs during view creation.

### Design note

Explain why a returned `DocumentId` is preferable to a view for long-lived selection state, while a view is preferable for immediate zero-copy rendering.



### Capstone defense

Repair a parser whose single lifetime unnecessarily couples source input to scratch state, then decide which results should borrow and which should own.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Derive elision and explicit relationships for one-source and multiple-source APIs.
- Use lifetime shortening and subtyping in ordinary covariant borrowed views without extending provenance.
- Design structs and enums containing references while accounting for temporary and drop scopes.
- Reject unnecessary lifetime coupling and choose owned output when retention must outlive input borrowing.

### Closed-book checkpoint

1. What does a lifetime parameter change at runtime?
2. Who chooses the concrete region for a generic lifetime parameter?
3. Expand the three elision rules.
4. When must an output lifetime be explicit?
5. Read `'long: 'short` in words.
6. What does `T: 'a` constrain?
7. Why can one lifetime for unrelated fields be a lossy model?
8. Why does `fn text(&self) -> &str` often return for less than the field's stored lifetime?
9. How can consuming `self` expose the stored lifetime?
10. Distinguish `&'static T`, `T: 'static`, and a leaked allocation.
11. Why can an ID be more usable than a reference into a mutable collection?
12. Why do ranges avoid a self-referential document index?

Practical check: write a zero-copy `split_once` record view and an owned conversion from memory, with correct lifetimes and no unnecessary annotation.

### Transfer defense

Repair a parser whose single lifetime unnecessarily couples source input to scratch state, then decide which results should borrow and which should own.

Your answer must include:

1. What does a lifetime parameter describe?
2. What owner does a returned reference point into?
3. Why should a query used only for comparison usually have no output lifetime?
4. What does `'long: 'short` state?
5. What does `T: 'a` state?
6. Why is `String: 'a` usually true?
7. Why does `&'b str: 'a` require `'b: 'a`?
8. Distinguish lifetime of `Config<'source>` from `'source`.
9. What can lifetime elision derive for a receiver method?
10. Why do string literals hide lifetime bugs?
11. When does one shared lifetime lose useful precision?
12. When is one shared lifetime adequate?
13. How can an enum retain two possible source lifetimes?
14. Why can no annotation return `&local_string`?
15. When should borrowed data become owned?

#### Answer notes

A lifetime names a validity relationship, not a clock duration. Output provenance comes from actual backing storage. Outlives bounds permit shortening; they do not prolong owners. Owned types with no embedded non-static references satisfy broad outlives bounds. Receiver elision ties output references to the receiver when the rules apply. Literals are `'static`, so use heap-owned nested test inputs. Separate lifetimes when operations need independent replacement/validity; unify when the common usable region is the intended contract. Own data when it must survive arbitrary source teardown or when lifetime complexity exceeds the benefit of borrowing.

#### Transfer task

Design a parsed log book whose records borrow one input buffer while annotations borrow a separate catalog. Add a method replacing annotations without shortening record data. Include one compile-fail local annotation case.
