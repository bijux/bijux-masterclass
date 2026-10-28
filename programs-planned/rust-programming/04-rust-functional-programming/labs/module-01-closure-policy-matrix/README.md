# Laboratory 31 — Closure Policy Matrix

This is the independent product for **Course 4, Module 31: Closures, Capture, and Callable Contracts**. Read the [module chapter](../../course-book/module-31-closures-capture-and-callable-contracts/index.md) and complete its [workbook](../../course-book/module-31-closures-capture-and-callable-contracts/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

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

> What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Closure Policy Matrix**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
