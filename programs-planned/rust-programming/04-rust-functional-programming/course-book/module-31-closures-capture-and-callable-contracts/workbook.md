# Workbook — Module 31: Closures, Capture, and Callable Contracts

[Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Closures, Capture, and Callable Contracts** without relying on surface syntax. Keep the module question in view: *What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Closures, Capture, and Callable Contracts** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-01/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-01/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-01/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-01/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-01/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-01/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-01/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-01/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

Begin with three built-in normalization modes and writes:

```rust
fn normalizers(counter: &mut usize) -> Vec<Box<dyn Fn(String) -> String + '_>> {
    vec![
        Box::new(move |text| text.trim().to_owned()),
        Box::new(move |text| {
            *counter += 1;
            text.to_ascii_lowercase()
        }),
        Box::new(move |text| text.replace(' ', "-")),
    ]
}
```

The calling code clones the same `String` before trying each callback and selects a mode by numeric index.

### First classify the failures

There are compiler-level, semantic, and architectural defects mixed together:

- several `move` closures compete to capture the same `&mut usize`;
- the callbacks consume `String` although normalization only needs to read text;
- numeric selection permits an invalid mode;
- a fixed closed set has been erased behind dynamic dispatch;
- one “normalizer” changes observable behavior according to call history;
- no name, law, or failure policy remains attached to a mode;
- cloning the input repairs ownership symptoms while preserving a poor API.

Do not start by adding `Rc<RefCell<_>>`. That would make the capture legal while worsening the contract.

### Repair sequence

1. Replace the closed registry with a `Normalization` enum.
2. Give the enum an inherent `apply(&self, input: &str) -> String` method.
3. Move instrumentation to the caller or to a separate wrapper whose statefulness is explicit.
4. Retain a generic closure boundary only for the product requirement that truly accepts a caller-supplied experimental transform.
5. Infer the weakest callback trait from invocation: `Fn` for repeatable read-only normalization, `FnMut` for explicit instrumentation, `FnOnce` for one-shot finalization.

### Prove the repair

Add tests for valid mode parsing, invalid-mode rejection, input reuse without cloning, and idempotence only for modes whose specification includes it. Add a compiler prediction showing why a closure that moves a captured report title during invocation cannot satisfy `FnMut`.

### Transfer question

Suppose plugins may register arbitrary normalizers at runtime in Course 8. Would a boxed callback become justified? State what changed: the participant set became open and heterogeneous. Dynamic dispatch then solves a real requirement rather than serving as a default callback container.

## Part 3 — Focused exercises

### Exercise 1 — Capture and capability table

For each closure below, identify the exact captured place, capture mode, callable traits it can implement, whether the binding must be mutable, and whether the outer value remains usable while the closure is alive. Predict before compiling.

```rust
let name = String::from("alpha");
let a = || name.len();

let mut hits = 0_u64;
let mut b = || { hits += 1; hits };

let payload = String::from("body");
let c = move || payload;

let prefix = String::from("id-");
let d = move |n: u32| format!("{prefix}{n}");
```

### Exercise 2 — Weakest sufficient bounds

Write signatures for three functions: `with_default` calls a fallback at most once; `map_all` invokes a transformer repeatedly without requiring state mutation; `number_all` invokes a stateful callback repeatedly. Use the weakest sufficient callable bound and explain why a stronger bound would reduce valid callers.

### Exercise 3 — Return one anonymous type

Implement `offsetter(offset: i64) -> impl Fn(i64) -> i64`. Then explain why a function whose two branches contain two different closure expressions cannot generally return `impl Fn(i64) -> i64`, even when both perform the same operation.

### Exercise 4 — Repair a borrow extended by storage

A program stores `let length = || values.len();`, then tries to `push` into `values`, and later calls `length`. Give three repairs and state the semantic tradeoff of each. At least one repair must not clone the vector.

### Exercise 5 — Generic storage versus boxed storage

Design a policy type that stores one normalizer and one scorer. Then describe the product change that would justify changing the scorer field from a generic type parameter to `Box<dyn FnMut(&Job) -> Score>`.

### Exercise 6 — Call ledger test

Write a test strategy that proves a normalizer runs before a scorer for every item, the scorer runs exactly once per item, and a fallback is not called on the successful path. Do not rely only on the final output value.



## Part 4 — Independent laboratory

This laboratory turns closure capability into observable product behavior. The executable surface is in `labs/module-01-closure-policy-matrix/README.md`.

### Product problem

A job evaluator has three callable boundaries with different invocation rights:

- a fallback factory is optional work and may consume an owned recovery token;
- a classifier runs once per input and may keep call-local state;
- a stored policy normalizes an owned label before scoring the resulting job.

Using `Fn` everywhere is not “safer.” It can reject valid consuming or mutating callables. Using `FnOnce` everywhere is also inaccurate because it communicates no repeated-call guarantee. Your implementation must make the weakest sufficient contract visible at each boundary.

### Pre-implementation capture ledger

Before coding, complete this table for every supplied closure:

| Boundary | Captured values | Capture access | Maximum calls | Required trait | Why weaker/stronger bounds are wrong |
|---|---|---|---:|---|---|
| fallback | | | | | |
| classifier | | | | | |
| normalizer | | | | | |
| scorer | | | | | |
| transfer finalizer | | | | | |

Then predict whether each closure is callable through `&F`, `&mut F`, or only by value. Compile only after the prediction is frozen.

### Required construction sequence

1. Implement `resolve_or_else` so the fallback is not evaluated for `Some` and may move a captured `String` out of its environment for `None`.
2. Implement `classify_all` over `&[T]`. Add a classifier that increments a counter and incorporates the call number into its output. The returned vector must preserve source order.
3. Implement `Policy<N, S>` without `Box<dyn Fn...>`. `evaluate` consumes jobs, passes each owned label through the normalizer, then lets the scorer inspect the normalized job.
4. Add a call-ledger test. Final output alone is insufficient because an implementation may call the normalizer twice and coincidentally produce the same text.
5. Implement the one-shot finalizer transfer task. It must accept a closure that consumes an owned suffix or token.

### Adversarial cases

Your tests must distinguish these defective implementations:

- `unwrap_or(fallback())`, which evaluates fallback eagerly;
- scoring before normalization;
- cloning the label before normalization and scoring the stale original;
- requiring `Fn` for a stateful classifier;
- boxing all callables despite one concrete callable type per policy;
- using global state for the call ledger.

At least one test must compile only because the public bound is exactly `FnOnce`, and another must require `FnMut` rather than `Fn`.

### Defense

Be prepared to answer:

1. Why does `move` describe capture ownership but not by itself determine `FnOnce`?
2. Why is the classifier allowed to mutate its environment but not its input items?
3. Which ownership transfer eliminates the need to clone labels?
4. What future requirement would genuinely justify `Box<dyn Fn...>`?
5. Which test proves call count rather than merely output equality?

The executable starter and reference implementation are in [module-01-closure-policy-matrix](../../labs/module-01-closure-policy-matrix/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

LedgerFlow will eventually contain several transformation stages, but Day 1 is deliberately narrower. The goal is to establish **three callable boundaries with different reuse and ownership contracts**. Do not build a registry of boxed callbacks merely because callbacks are involved. The core should remain generic while each call site has one concrete callable type.

### Product slice

A raw event label may need normalization before parsing or reporting. A normalized event may then be classified repeatedly. A completed diagnostic batch is finally consumed to produce one report. These are different products:

- normalization is repeatable and read-only;
- classification may update local instrumentation across calls;
- finalization consumes its batch and may consume captured configuration.

Represent that distinction in signatures rather than comments alone.

### Implement the three boundaries

Add functions equivalent in responsibility to:

```rust
fn normalize_label<F>(raw: &str, normalize: F) -> String
where
    F: Fn(&str) -> String;

fn classify_events<'a, I, F>(events: I, classify: F) -> Vec<Classification>
where
    I: IntoIterator<Item = &'a NormalizedEvent>,
    F: FnMut(&NormalizedEvent) -> Classification;

fn finish_batch<F>(batch: DiagnosticBatch, finish: F) -> Report
where
    F: FnOnce(DiagnosticBatch) -> Report;
```

The exact names may differ, but the semantics may not. Do not add a stronger bound than the implementation needs. A function that invokes a callback once must not demand `Fn` merely because the supplied closure happens to implement it.

### Produce a capture ledger

Before coding, fill one row per closure used in the increment:

| Closure | Captured place | Capture mode | Why captured | Callable capability | Expected calls | Can escape creator? |
|---|---|---|---|---|---:|---|

A `move` closure does not automatically consume every captured value when called. Record whether values are copied, borrowed, mutably borrowed, or moved into the closure, then separately determine whether the body moves a captured value out during invocation.

### Required experiments

1. Supply a capture-free function item to the normalizer.
2. Supply a closure that borrows immutable configuration.
3. Supply a classifier that mutates a call counter and record the exact call order.
4. Supply a finalizer that moves a captured `String` into the returned report, proving why it is `FnOnce`.
5. Attempt one deliberately overstrong callback signature, record the compiler consequence, and repair the boundary rather than adding clones.

### Required tests
The increment is not proved by “the callback ran.” Add tests that establish:

- normalization receives the expected borrowed text and is called exactly once per input;
- classification preserves source order and has the expected call count;
- a stateful classifier is isolated to the call that owns it;
- the one-shot finalizer can consume captured state;
- no callback is invoked when an earlier precondition rejects the operation;
- a repeatable normalizer gives the same result for repeated equal inputs when its documented law requires that behavior.

Do not claim normalizers are universally idempotent. State the precondition and test only the built-in modes for which `n(n(x)) == n(x)` is part of the contract.

### Rejected shortcuts

Reject these designs in your design note:

- `Vec<Box<dyn Fn...>>` for a fixed, closed set of built-in modes;
- accepting `String` when the callable only needs `&str`;
- forcing `Fn` for a callable invoked once;
- inserting `move` without a capture audit;
- hiding classification history inside a globally shared counter.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can derive capture mode and the weakest callable bound from the body, predict whether storage extends a borrow, and test the promised invocation count.

### Closed-book retrieval

1. A closure uses an owned `String` only through `len()`. Which callable traits can it implement after `move` capture, and why?
2. A closure increments a captured counter. Which trait is the weakest honest bound for repeated calls?
3. A closure returns a captured `String` by value. What changes after the first call?
4. Why can a noncapturing closure coerce to a function pointer while a capturing closure cannot?
5. How can storing a closure extend the lifetime of a borrow that an immediate call would end sooner?
6. What is the difference between moving a mutable reference into a closure and moving the referent?
7. When is `Box<dyn FnMut(...)>` justified, and what costs and constraints does it introduce?
8. Why is `F: FnOnce()` not evidence that the caller must consume the closure immediately?
9. How do capture precision and place expressions affect partial-field use?
10. Why is `Fn` an overconstraint for a callback that the implementation calls only once?

### Reconstruction task

From an empty file, implement `apply_twice`, a consuming fallback, and a stored mutable callback. Annotate every capture and explain why each API uses `Fn`, `FnMut`, or `FnOnce`.

### Transfer task

Design a callback boundary for a retrying job runner: one callback observes every attempt, one may mutate retry statistics, and one consumes a recovery token after final failure. Produce:

- capture ledger showing borrow, mutable borrow, or move for each captured value;
- call-count contract and selected `Fn` capability;
- one retained-closure lifetime constraint;
- test proving the callback is not invoked more often than promised;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.
