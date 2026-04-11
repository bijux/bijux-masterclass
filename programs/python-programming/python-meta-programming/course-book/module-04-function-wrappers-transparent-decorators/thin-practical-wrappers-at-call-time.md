# Thin Practical Wrappers at Call Time

Once the definition-time mechanics are clear, the next question is practical:

> what kinds of wrapper behavior are still thin enough to stay transparent?

This page uses small real decorators to answer that question. The common pattern is:

- do a small amount of pre- or post-call work
- delegate to the original function
- preserve return values and exception behavior unless the wrapper explicitly says otherwise

## The sentence to keep

When reviewing a thin wrapper, ask:

> what small call-time behavior was added, and what parts of the original callable still
> remain unchanged?

If that answer stays short and explicit, the wrapper is often still thin.

## Thin wrappers change behavior without owning policy-heavy state

A thin wrapper may:

- record timing
- emit a warning
- log a call

What keeps it thin is not zero behavior change. It is that the wrapper's concern stays
narrow and does not quietly take ownership of larger runtime policy.

## A timing wrapper is a good first example

```python
import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")

    return wrapper
```

This wrapper adds one narrow behavior:

- measure duration around the call

It still:

- delegates to the original function
- returns the original result
- lets exceptions propagate after reporting timing

That is a good example of thin behavior with a clear cost model.

## A deprecation wrapper is another thin pattern

```python
import functools
import warnings


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated; use an alternative.",
            DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return wrapper
```

This wrapper changes the call boundary too, but in a still-reviewable way:

- it signals lifecycle status
- it delegates the real behavior unchanged

That is thin enough when the warning behavior is explicit and the wrapper does not start
rewriting semantics underneath the caller.

## Call-time behavior should be easy to name

Thin wrappers are easier to trust when the call-time effect can be summarized in one
sentence:

- "times the call"
- "logs the call"
- "warns once per use"

The moment the explanation becomes much longer, the design may already be moving beyond a
thin wrapper and toward policy.

## `try/finally` often matters for transparency

For wrappers like timers, the right control-flow shape is important:

```python
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print("timing recorded")
```

Without `finally`, exceptions can skip the post-call behavior and make the wrapper's
behavior less honest or less useful.

That is a good example of quality in wrapper design: small details change whether the
wrapper tells the truth about what it does.

## Exception transparency is part of being thin

Thin wrappers should usually preserve the original exception model:

- they may observe the failure
- they may record timing or emit a warning
- they should not silently swallow or rewrite exceptions unless that change is the entire documented purpose

This keeps the wrapped callable legible to both callers and reviewers.

## Thin does not mean free

Even narrow wrappers still add:

- call overhead
- stack frames
- trace and debugging complexity
- potential tooling impact if metadata preservation is sloppy

The point of calling them thin is not to pretend they are free. It is to say the added
behavior is still narrow, inspectable, and reviewable.

## Thin wrappers are the lower-power decorator case

This matters for the course's power ladder:

- if the concern is narrow and per-call, a thin decorator is often a reasonable choice
- if the concern starts collecting state, retries, caching, or cross-cutting policy, the review burden goes up quickly

That boundary is the reason the next page exists.

## Review rules for thin practical wrappers

When reviewing thin wrappers, keep these questions close:

- can the added call-time behavior be named in one short sentence?
- does the wrapper still delegate result and exception behavior honestly?
- is `try/finally` used when post-call behavior should still happen on failure?
- is the wrapper doing narrow observation or signaling, rather than taking ownership of larger policy?
- does the wrapper already feel like a small framework disguised as a decorator?

## What to practice from this page

Try these before moving on:

1. Implement a timing decorator that still reports duration when the wrapped function raises.
2. Implement a deprecation decorator with `stacklevel=2` and explain why the caller frame matters.
3. Write down one example of a thin wrapper and one example that already feels too stateful to stay on this page.

If those feel ordinary, the next step is to study the stateful boundary directly.

## Continue through Module 04

- Previous: [Decorator Syntax and Definition-Time Rebinding](decorator-syntax-and-definition-time-rebinding.md)
- Next: [Stateful Wrappers and Semantic Drift](stateful-wrappers-and-semantic-drift.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
