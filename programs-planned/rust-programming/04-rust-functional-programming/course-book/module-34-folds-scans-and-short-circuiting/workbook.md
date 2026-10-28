# Workbook — Module 34: Folds, Scans, and Short-Circuiting

[Return to the chapter](index.md) · [Open the LedgerFlow engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether you can use **Folds, Scans, and Short-Circuiting** without relying on surface syntax. Keep the module question in view: *What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?* For every task, identify the program point where the decisive type, ownership, dispatch, failure, or cost relationship is established. Compile only after committing to a prediction, and preserve the smallest counterexample that changes your model.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Folds, Scans, and Short-Circuiting** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`case-01.rs`](../../compiler-labs/module-04/case-01.rs) | Pass or fail? What exact rule decides? |
| 2 | [`case-02.rs`](../../compiler-labs/module-04/case-02.rs) | Pass or fail? What exact rule decides? |
| 3 | [`case-03.rs`](../../compiler-labs/module-04/case-03.rs) | Pass or fail? What exact rule decides? |
| 4 | [`case-04.rs`](../../compiler-labs/module-04/case-04.rs) | Pass or fail? What exact rule decides? |
| 5 | [`case-05.rs`](../../compiler-labs/module-04/case-05.rs) | Pass or fail? What exact rule decides? |
| 6 | [`case-06.rs`](../../compiler-labs/module-04/case-06.rs) | Pass or fail? What exact rule decides? |
| 7 | [`case-07.rs`](../../compiler-labs/module-04/case-07.rs) | Pass or fail? What exact rule decides? |
| 8 | [`case-08.rs`](../../compiler-labs/module-04/case-08.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 04-rust-functional-programming
```

## Part 2 — Diagnose and repair

A reducer uses this accumulator:

```rust
(records.iter()).fold(
    (0usize, 0i64, 0i64, Vec::<String>::new(), false),
    |(count, min, total, mut errors, stop), record| {
        // updates external account state here
        // pushes string errors here
        // wraps on overflow in release builds
        // uses stop for both error and successful discovery
        (count + 1, min.min(record.amount), total + record.amount, errors, stop)
    },
)
```

The tuple shape hides the invariant. Empty input reports a minimum of zero, overflow policy depends on build behavior, diagnostics lose source structure, and mutation outside the accumulator may remain after a later check fails.

### Recover the invariant

Before touching syntax, state what each prefix means. Then define a named accumulator with `Option<i64>` for min/max, checked totals, accepted count, and typed diagnostics. If account state is updated, place a candidate copy or validated delta inside the transition so publication occurs only after all checks pass.

### Separate three meanings of stopping

- `Result`/`try_fold`: invalid transition, fail now.
- explicit report accumulator: continue and retain diagnostics.
- `ControlFlow::Break(found)`: successful early discovery.

One Boolean cannot communicate all three.

### Repair method

1. Implement a simple loop with explicit checks.
2. Add prefix tests after every item.
3. Convert to `try_fold` only if the accumulator remains readable.
4. Use `scan` for a timeline rather than mutating a vector from the fold.
5. Keep the event that caused overflow in the error value.

### Adversarial proof

Test empty input, one negative value, exact integer boundary, overflow, and an invalid event after several valid prefixes. Confirm that the published ledger equals the last valid prefix and that no external state changed from the rejected event.

The clinic passes when you can explain the invariant without naming `fold`. The consumer is an implementation choice; the prefix contract is the design.

## Part 3 — Focused exercises

### Exercise 1 — Prove a summary fold

Design a `Summary { count, total, min, max }` fold for signed amounts. State the empty-prefix invariant, one-step preservation, and overflow policy before writing code.

### Exercise 2 — Choose fold, reduce, or sum

For four domains—nonempty greatest common divisor, optional maximum, monetary total with checked overflow, and string concatenation—choose a reduction form and explain empty-input and order policy.

### Exercise 3 — Running balance with `scan`

Given deposits and withdrawals, produce a lazy running-balance stream. Decide what happens at insufficient funds and whether the failing event is consumed.

### Exercise 4 — Failure-atomic `try_fold`

Apply account events with `try_fold`. A failed event must leave the externally visible ledger unchanged. Explain why mutating an outer `HashMap` inside the closure is a weaker design.

### Exercise 5 — Early exit is not always failure

Find the first prefix whose total reaches a quota and return both index and total. Use `ControlFlow` and explain why `Result` would distort the domain.

### Exercise 6 — Split accumulator soup

A one-pass fold tracks account state, diagnostics, audit text, progress output, and timing. Refactor the design without automatically making five passes.



## Part 4 — Independent laboratory

The crate in `labs/module-04-streaming-metrics/README.md` asks for four related but different traversals. Treat them as separate contracts.

### Prefix invariant first

For `Metrics`, state the invariant after consuming exactly `k` values:

- `count` equals `k`;
- `total` equals the checked sum of the first `k` values;
- `minimum` and `maximum` are `None` exactly when `k == 0`;
- otherwise extrema describe precisely that prefix.

Do not begin with a tuple accumulator. The named state is part of the proof surface.

### Four traversal modes

#### Final summary

Implement `summarize` with `try_fold`. Overflow must return `MetricError::Overflow` and no partial final `Metrics`. Test empty input, mixed signs, and overflow at both the first and a later step.

#### Running totals

Implement a lazy `scan` that yields each checked prefix total. Decide what happens after overflow. The published contract emits exactly one error item and then remains exhausted. A scan that repeatedly emits errors is wrong even if the first error is correct.

#### First threshold crossing

Use `ControlFlow` to return the first `(index, prefix_total)` above a limit. Crossing is an ordinary discovery, not a domain error. Checked addition can still produce an error. Your type shape must preserve that distinction.

#### Sign-change transfer reducer

Define whether zero is its own sign class or ignored. State the policy before coding, encode it in a named accumulator, and write a counterexample that distinguishes the two interpretations.

### Diagnostic experiment

For `[2, 4, 8]` and limit `5`, record accumulator state before and after every closure call. For `[i64::MAX, 1, 2]`, record which items are pulled by each traversal. This is evidence about short-circuiting, not merely output.

### Rejected implementations

- minimum initialized to zero;
- wrapping or saturating arithmetic without product authorization;
- an external mutable diagnostics vector captured by a fold;
- one Boolean used for both “error seen” and “stop requested”;
- `reduce` for an operation that requires an explicit empty identity;
- a five-field anonymous tuple whose positions have no reviewable names.

### Defense

You must explain why `try_fold` failure is not transactionality for external effects, why `scan` can remain lazy while carrying state, and why a readable loop would be preferable if the accumulator update required several independently fallible substeps.

The executable starter and reference implementation are in [module-04-streaming-metrics](../../labs/module-04-streaming-metrics/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

## Part 5 — Capstone transfer

Day 4 creates ledger state from accepted events. A reducer is trustworthy only when you can state what its accumulator means after every processed prefix. Begin with that sentence. Do not begin with `fold`.

### Define the accumulator invariant

Write an invariant equivalent in precision to:

> After processing the first `k` accepted events, each account balance equals the checked sum of those `k` events for that account, every applied event appears once in audit order, and no state from event `k + 1` or later is observable.

Adapt it to the actual domain. Identify which fields are derivable, which are authoritative, and which conditions make a transition invalid.

### Implement a named accumulator

Avoid tuple accumulators such as `(BTreeMap<_, _>, Vec<_>, usize, bool)`. Create a named type whose fields encode the reducer state and whose methods preserve the invariant. Keep candidate mutation local until every check for the current event succeeds.

Checked arithmetic is mandatory. The event that causes overflow must remain available for the diagnostic. Do not update one account and then discover that another part of the transition is invalid.

### Three reduction modes

Implement and contrast three consumers:

#### 1. Fail-fast application

Use `try_fold` or an equally explicit loop. The first illegal transition stops reduction. Document what state is returned or discarded. Do not call the first error “accumulated diagnostics.”

#### 2. Continue-with-diagnostics inspection

Visit every accepted event, retaining valid state transitions and structured diagnostics for rejected transitions according to the published policy. Use a named report accumulator; do not mutate an unrelated external vector from inside the fold.

#### 3. Normal early discovery

Implement one query with `ControlFlow`, such as finding the first event that causes an account to cross a threshold. Crossing is a successful discovery, not an error. Preserve that distinction in the return type.

### Timeline with `scan`

Add a borrowed or owned timeline iterator that yields the account state after each accepted event. State whether the initial state is yielded. State whether an invalid event terminates the timeline, yields a diagnostic item, or is excluded by an earlier stage.

### Prefix proof tests

For several short sequences, compare every emitted prefix state with a simple trusted reference calculation. Include:

- empty input;
- one event;
- multiple accounts;
- an exact boundary value;
- arithmetic overflow;
- an illegal transition after valid prefixes;
- a later valid event in accumulation mode.

The test should identify the shortest prefix at which a defect appears.

## Part 6 — Reconstruct and defend

Do not advance because the calendar day ended. Advance when all hard evidence is present.

### Advancement decision

Advance only when you can state the accumulator invariant for every prefix, select the correct empty-input policy, and identify the exact state returned on short circuit.

### Closed-book retrieval

1. What is true of a valid fold accumulator after the empty prefix?
2. Why is `reduce` unable to represent an empty-input identity on its own?
3. When should `maximum` be `Option<T>`?
4. How does `scan` differ from `fold` in output shape?
5. What residual controls `try_fold` short-circuiting?
6. When is `ControlFlow::Break` more accurate than `Err`?
7. Why can external mutation make a fallible fold non-atomic?
8. How do floating-point order and integer overflow policy affect reductions?
9. What makes an accumulator “soup”?
10. When is an explicit loop easier to prove than a combinator?

### Reconstruction task

Implement count, checked sum, min, max, and running mean in one named accumulator. Add a `try_fold` variant that stops on overflow without mutating external state.

### Transfer task

Aggregate telemetry until either a threshold is crossed or malformed input appears, while retaining the last valid prefix summary. Produce:

- accumulator type and prefix invariant;
- stopping condition and state returned at early exit;
- overflow and empty-input policy;
- test that distinguishes `fold`, `try_fold`, `scan`, or an explicit loop;

### Spaced review

Repeat questions 2, 4, 7, and 10 after 24 hours. Repeat the reconstruction after seven days with a different domain.
