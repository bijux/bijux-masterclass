# Workbook — Module 13: Scoped Access and Escape Prevention

[Chapter](index.md) · [Laboratory](../../labs/module-03-scoped-visitors/README.md) · [Memory Workspace guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Scoped Access and Escape Prevention** has become a usable model rather than remembered vocabulary. Its governing question is: *Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?* Preserve your first prediction and record decisive facts in a **scope and escape table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 12 — Lifetime Relationships and Borrowed APIs that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?**
3. Draw the smallest **scope and escape table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Scoped Access and Escape Prevention** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-hrtb-owned-result.rs`](../../compiler-labs/module-03/01-hrtb-owned-result.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-hrtb-reference-escape.rs`](../../compiler-labs/module-03/02-hrtb-reference-escape.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-fnonce-consumes-capture.rs`](../../compiler-labs/module-03/03-fnonce-consumes-capture.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-fnmut-captured-counter.rs`](../../compiler-labs/module-03/04-fnmut-captured-counter.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-scratch-view-return.rs`](../../compiler-labs/module-03/05-scratch-view-return.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-owned-ranges-escape.rs`](../../compiler-labs/module-03/06-owned-ranges-escape.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-naive-self-reference.rs`](../../compiler-labs/module-03/07-naive-self-reference.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-opaque-borrowed-iterator.rs`](../../compiler-labs/module-03/08-opaque-borrowed-iterator.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 02-rust-ownership-lifetimes-memory
```

## Part 2 — Diagnose and repair

A tokenizer was designed to reuse one internal `String`, but its author wanted an iterator of `&str`. After borrow errors appeared, the implementation was changed to clone every token and leak the strings so they could be returned as `'static`.

### Diseased design

```rust
struct Tokenizer {
    scratch: String,
}

impl Tokenizer {
    fn token(&mut self, raw: &str) -> &'static str {
        self.scratch.clear();
        self.scratch.push_str(raw.trim());
        Box::leak(self.scratch.clone().into_boxed_str())
    }
}
```

This compiles, but every call permanently leaks an allocation. The `'static` return lies about the intended product lifecycle. The scratch buffer no longer provides its claimed allocation-reuse benefit because it is cloned each time.

### Repair path A: owned output

When callers need to retain tokens independently, return `String`. Reuse of scratch may no longer matter; measure before retaining complexity.

```rust
fn token_owned(raw: &str) -> String {
    raw.trim().to_owned()
}
```

### Repair path B: borrow caller input

If normalization is only trimming, return a slice of the input:

```rust
fn token_borrowed(raw: &str) -> &str {
    raw.trim()
}
```

No tokenizer state is needed.

### Repair path C: scoped scratch access

If transformation genuinely requires scratch storage:

```rust
impl Tokenizer {
    fn with_token<R>(
        &mut self,
        raw: &str,
        operation: impl for<'token> FnOnce(&'token str) -> R,
    ) -> R {
        self.scratch.clear();
        self.scratch.extend(raw.chars().flat_map(char::to_lowercase));
        operation(&self.scratch)
    }
}
```

The callback can compute an owned result but cannot retain the token. The mutable borrow of the tokenizer lasts through the callback, so reentrant calls are impossible in safe code.

### Clinic tasks

1. State the actual retention requirement for three callers: comparison, indexing, and long-term storage.
2. Choose one repair for each caller and justify allocation behavior.
3. Add a negative test showing that scoped token references cannot escape.
4. Explain what happens if the callback panics after `scratch` has changed.
5. Decide whether the tokenizer should preserve its previous scratch contents after panic. If yes, defer the transactional repair to Module 14.

The lesson is not that callback APIs are always superior. It is that ownership requirements must be classified before lifetime syntax is selected.

## Part 3 — Focused exercises

### Access protocol

Attempt every required exercise and commit the attempt before opening `exercise-answers.md`. Mark each as:

### Exercise 1 — Quantifier translation

Translate each signature into precise prose:

```rust
fn a<'x, F>(x: &'x str, f: F) where F: FnOnce(&'x str);
fn b<F>(x: &str, f: F) where F: for<'x> FnOnce(&'x str);
fn c<R, F>(x: &str, f: F) -> R where F: for<'x> FnOnce(&'x str) -> R;
```

State which forms can permit a returned or stored borrow and under what surrounding type constraints.

### Exercise 2 — Capture matrix

For six closures, determine whether each implements `Fn`, `FnMut`, and `FnOnce`, and whether `move` changes that result. Include one closure that reads owned state, one that mutates a counter, and one that consumes a captured `String`.

### Exercise 3 — Escape attempt

Write a `visit_lines` function with an HRTB. Attempt to collect `&str` lines outside the call. Preserve the compiler diagnostic in your journal, then collect byte ranges instead.

### Exercise 4 — Early termination

Implement scoped line traversal using `ControlFlow`. Stop at the first line containing a query and return its line number, not a borrowed line.

### Exercise 5 — Ordinary iterator comparison

Implement immutable tokenization over caller-owned text as both an iterator return and a visitor. Compare composability, allocation, escape behavior, and diagnostic quality. Select the simpler public API.

### Exercise 6 — Scratch transformation

Build a reusable lowercase scratch transformer with `with_transformed`. Prove through a compile-fail specimen that a caller cannot retain the transformed slice.

### Exercise 7 — Replace self-reference

Refactor a proposed `Document { text: String, title: &str }` into:

1. recomputation;
2. a validated `Range<usize>`;
3. a separate borrowed `DocumentView<'a>`.

State mutation invariants for each.

### Exercise 8 — Opaque lifetime expansion

Expand the concrete conceptual captures of an iterator returned by:

```rust
fn matching(&self, query: &str) -> impl Iterator<Item = &str> + '_;
```

Decide whether the displayed signature is sufficient on your toolchain and write an explicit version that documents both sources.

### Exercise 9 — API review

Review a callback API that uses `for<'a>` even though it passes an owned `String`. Remove lifetime machinery and explain why the original bound proved nothing useful.

### Exercise 10 — Capstone reasoning

Design `Workspace::visit_matches` so match views cannot escape. Compare it with `Workspace::matches`, which returns a normal iterator borrowing immutable documents. Specify when each is appropriate.

### Interleaved reasoning pass

1. For **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the scope and escape table.
2. For **Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the scope and escape table.
3. For **Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the scope and escape table.
4. For **Use callbacks and scoped APIs to prevent temporary references or brands from escaping**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the scope and escape table.

5. Identify one guarantee from an earlier course that a careless implementation of **Scoped Access and Escape Prevention** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product

Build `ScopedText`, a safe text-processing component that owns one reusable scratch buffer and exposes transformed records only inside callback scope.

The executable surfaces are under:

```text
labs/module-03-scoped-visitors/
├── starter/
└── solution/
```

### Required behavior

`ScopedText` must provide:

```rust
pub struct ScopedText { /* private */ }

impl ScopedText {
    pub fn new() -> Self;

    pub fn with_normalized<R>(
        &mut self,
        raw: &str,
        operation: impl for<'view> FnOnce(&'view str) -> R,
    ) -> R;

    pub fn visit_words<F>(&mut self, raw: &str, visitor: F)
    where
        F: for<'word> FnMut(&'word str);
}
```

Normalization trims leading/trailing whitespace, collapses each run of Unicode whitespace to one ASCII space, and lowercases characters with Rust's Unicode lowercase expansion. `visit_words` must expose words from the normalized scratch buffer without allocating one `String` per word.

### Adversarial cases

Use Turkish dotted capital I, German sharp-s behavior as provided by Unicode lowercase mappings, empty input, and a string with several kinds of whitespace. Do not promise locale-aware case folding; state exactly what `char::to_lowercase` provides.

### Acceptance

```bash
cargo test -p rust-olm-lab-03-scoped-visitors --all-targets
cargo clippy -p rust-olm-lab-03-scoped-visitors --all-targets -- -D warnings
```

A solution fails conceptually if it returns references into scratch storage or leaks memory even if its positive tests pass.

### Tiered hints

Do not open a later tier until the previous tier has produced a written attempt.

- **Hint 1 — concept:** return to the governing question: Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?
- **Hint 2 — topology:** draw owners/borrows/states/errors before changing syntax; identify the one boundary that should own the invariant.
- **Hint 3 — structure:** separate validation from mutation and pure transformation from effects. Use the standard operation that encodes the safety fact before inventing an abstraction.
- **Hint 4 — implementation-adjacent:** consult only the relevant standard-library or Reference page; do not open `solution/src`.

The executable starter and reference implementation are in [module-03-scoped-visitors](../../labs/module-03-scoped-visitors/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Scoped Visitors**, record:

- the public behavior that demonstrates **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

### Outcomes mapped

- Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.
- Read and design for<'a> higher-ranked callback bounds as universal quantification over borrow duration.
- Account for closure capture and Fn, FnMut, and FnOnce requirements at scoped boundaries.
- Use callbacks and scoped APIs to prevent temporary references or brands from escaping.
- Recognize self-reference pressure and choose indices, owned state, callbacks, or later pinning only when justified.

Extend `memory-workspace` with search operations that distinguish transient observation from durable evidence.

### Borrowed view

A `MatchView<'a>` may contain:

- a `DocumentHandle` copied by value;
- a borrowed document title;
- a borrowed matched slice;
- a byte `Range<usize>`.

A method that returns an ordinary iterator may tie views to an immutable workspace borrow. While that iterator remains usable, mutating the workspace must be rejected.

### Scoped visitor

Also provide a visitor route whose callback is higher-ranked when the implementation uses a temporary normalization buffer. The callback may update counters or copy ranges, but cannot retain the temporary normalized text.

### Durable edit input

Any later mutation must use `DocumentHandle` plus a validated byte range, not a stored `&str`. This keeps edits independent of the address of a `String` control block and allows stale-handle detection.

### Required tests

1. a returned ordinary iterator keeps the workspace immutably borrowed;
2. a scoped normalized match cannot escape;
3. an owned handle/range pair can survive the read operation;
4. mutation validates the generation and range against current content;
5. no `'static` annotation or leaked allocation appears.

### Design defense

Explain why the workspace offers both APIs. If both implementations use immutable stable backing data and the visitor adds no retention boundary, remove the visitor. The capstone must not retain complexity merely because the module taught it.

### Capstone defense

Design a scratch-buffer decoder that lends temporary output to arbitrary callbacks but cannot return a reference into the scratch allocation.

### Capstone invariant trace

For the Module 13 Memory Workspace increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Complete this checkpoint closed-book. Compiler access is allowed only after the prediction portion has been committed.

### Outcome reconstruction

For each outcome, write a claim, one example, one non-example, and one limitation.

Without reopening the chapter, reconstruct the outcomes for **Module 13: Scoped Access and Escape Prevention**. Compare your list with the earlier outcome map only after writing it, then mark each item as modelled, predicted, repaired, built, transferred, or still unsupported.

### Closed-book checkpoint

Pass without notes.

1. Translate `F: for<'a> FnMut(View<'a>)` into who chooses what and when.
2. Explain why `R` in `for<'a> FnOnce(&'a str) -> R` cannot normally be that borrowed `str`.
3. Distinguish `move` capture from `FnOnce` call behavior.
4. Explain why a callback can be higher-ranked over its argument while borrowing captured state itself.
5. Give one traversal ordinary `Iterator` models well and one scratch-buffer traversal it does not.
6. Repair a self-referential text index using ranges.
7. Identify every lifetime captured by an opaque iterator over borrowed data.
8. Reject `Box::leak` as a routine lifetime repair with a resource argument.
9. Produce one negative compiler specimen proving escape prevention.
10. Defend whether the capstone actually needs a scoped visitor.

The module is incomplete if you can reproduce `for<'a>` syntax but cannot explain the quantifier order or design a simpler owned/borrowed alternative.

### Transfer defense

Transfer **Module 13: Scoped Access and Escape Prevention** to a product unrelated to the course capstone. Change the domain model and failure mode, preserve the governing relationship, and identify which part of the original design was essential rather than accidental.

Your answer must include:

- the governing rule for **Module 13: Scoped Access and Escape Prevention** in plain language;
- state, ownership, or authority before and after the decisive operation;
- one causal negative case that fails for the intended reason;
- one principled repair and one easier repair that deletes a requirement;
- the limit of the evidence you used;
- one transfer to a product with different data and failure behavior.


1. Read `for<'a> FnOnce(&'a T) -> R` aloud.
2. Who chooses `'a`?
3. Why can `R = usize` work?
4. Why can fixed `R = &'a T` not be selected outside the quantifier?
5. How can an element reference borrowing external input escape a local list?
6. Why can the local list slice not escape?
7. Which closure trait accepts consuming captures?
8. What changes when a callback may be invoked repeatedly?
9. How does panic affect local scratch?
10. Why is `RefCell` guard scope relevant to callbacks?
11. What is a generative lifetime?
12. Why are nested scoped invocations distinct?
13. When is a handle better than a callback?
14. When is owned return better?
15. What negative evidence is required?

#### Answer notes

The callback must work for every callee-chosen lifetime. Results independent of that lifetime escape normally. Nested provenance allows external borrows to escape while local-container borrows cannot. `FnOnce` is weakest for one invocation. Panic drops local resources; a guard must restore pooled protocol state. Use handles for durable identity and owned returns for durable data. A compile-fail test must isolate the intended escape prohibition.

#### Transfer task

Build `with_rows` over a temporary parsed row vector whose cells borrow external CSV text. Return an owned aggregate and, in a separate API, permit copying one external cell reference. Explain both lifetime layers.

### Closed-book defense

In five minutes, answer “Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?” using the **scope and escape table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Memory Workspace. A list of APIs without the deciding relationship is incomplete.
