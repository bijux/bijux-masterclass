# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that keep
wrapper power, policy scope, and typing limits honest.

## Answer 1: Build one decorator factory with real configuration

Example answer:

```python
import functools


def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator
```

Strong explanation:

- `repeat(times)` runs once at definition time
- the returned decorator captures `times`
- the wrapper uses that captured value on each call

Good conclusion:

This is an honest factory because the configuration is explicit and the captured policy is
still narrow and visible.

## Answer 2: Review one resilience wrapper

Example answer:

A retry decorator that retries `ConnectionError` up to three times changes semantics in at
least three ways:

- it may call the underlying function more than once
- it waits between attempts
- it changes when failure becomes final

Good conclusion:

That is already control-flow policy, not a thin wrapper, because the decorator now governs
execution timing and error handling.

## Answer 3: Validate one narrow hint subset

Example answer:

Support:

- plain runtime classes
- `Union`
- `Optional`
- `Any`

Reject:

- parameterized generics such as `list[int]`

Good conclusion:

This is an honest partial validator because it names its supported surface clearly and
refuses unsupported hints instead of pretending to understand them.

## Answer 4: Inspect cache policy instead of only cache speed

Example answer:

```python
import functools


@functools.lru_cache(maxsize=2, typed=True)
def add(x, y):
    return x + y
```

Strong explanation:

- `typed=True` distinguishes calls such as `add(1, 2)` and `add(1.0, 2)`
- `cache_info()` exposes hits, misses, and current size
- `cache_clear()` provides deterministic reset

Good conclusion:

The cache is not just a speed trick. It owns keying, eviction, and operational state, and
those choices are part of the wrapper's public meaning.

## Answer 5: Reject one decorator that grew too large

Example answer:

Suppose one decorator tries to combine:

- retries
- timeouts
- logging
- validation
- cache invalidation

Strong redesign:

- keep a thin boundary decorator if needed
- move retry policy to a retry object or client wrapper
- move validation to a validator component
- move cache ownership to an explicit cache service or standard-library wrapper

Good conclusion:

Once policy becomes this broad, a single decorator hides too much state and coordination to
stay reviewable.

## Answer 6: Review a partial validator honestly

Example answer:

A partial `@validated` decorator can honestly claim:

- it checks a narrow supported hint subset at one runtime boundary
- it binds arguments before validating
- it may raise or warn on mismatch

It cannot honestly claim:

- full typing support
- safety in warning mode
- enforcement of every advanced typing feature

Good conclusion:

Warning mode is not safety mode because the wrapped function may still fail internally even
after the validator chooses not to raise.

## What strong Module 05 answers have in common

Across the whole set, strong answers share the same habits:

- they distinguish thin wrappers from policy-carrying wrappers
- they keep runtime typing claims narrow and explicit
- they expose reset, inspection, or control hooks when stateful policy exists
- they move overloaded decorator behavior into explicit owners when the wrapper boundary is no longer the clearest fit

If an answer still sounds like "the decorator can just handle it," revise it until you can
say what policy it owns, what it refuses to own, and why that boundary is honest.
