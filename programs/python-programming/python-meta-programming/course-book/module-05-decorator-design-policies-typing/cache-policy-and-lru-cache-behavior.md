# Cache Policy and lru_cache Behavior

Caching is one of the clearest examples of a decorator crossing from thin transformation
into operational policy.

The wrapper no longer only changes what happens around a call. It changes whether the
original function runs at all, how memory is used over time, and what operational hooks
the system needs.

## The sentence to keep

When reviewing a cache decorator, ask:

> what keying rule, eviction policy, and reset surface does this wrapper now own?

That question keeps caching tied to observable semantics instead of treating it like a
performance flourish.

## Cache policy is about more than a dictionary

The important cache questions are not only implementation details:

- how are keys constructed?
- what inputs are allowed?
- when are entries evicted?
- how can the cache be inspected or cleared?
- what happens under concurrency?

Those are policy decisions. A decorator that answers them is carrying real runtime
ownership.

## `functools.lru_cache` is the reference point

For this module, the standard-library cache matters for three main reasons:

1. it defines a clear keying story
2. it defines a clear least-recently-used eviction story
3. it exposes operational hooks such as `cache_info()` and `cache_clear()`

That last point is especially important. A serious cache should not hide its own state
completely from tuning, debugging, or tests.

## One picture of cache behavior

```text
call -> make key -> cache hit? -> return cached value
                    cache miss -> call original -> store according to policy -> return value
```

That loop looks simple, but every box in it carries design choices.

## Key construction is part of correctness

If the keying rule is wrong, the cache is wrong.

That is why Module 05 keeps saying:

- key construction is not a mere optimization detail
- it is part of the meaning of the wrapper

For `lru_cache`, the key path is carefully defined for hashable arguments, with optional
`typed=True` behavior that keeps `1` and `1.0` separate when desired.

That is much stronger than an ad hoc stringification trick hidden in a custom decorator.

## Eviction policy should be explicit

With `lru_cache`, capacity limits and least-recently-used eviction are part of the public
shape of the decorator.

That matters because eviction changes semantics over time:

- old calls may stop being cached
- hit and miss behavior depends on usage history
- memory growth is bounded only when capacity policy exists

So a cache wrapper is never only "speed." It is state plus history plus policy.

## Operational hooks make cache state reviewable

One of the strongest parts of the standard-library design is the explicit hook surface:

- `cache_info()` for hits, misses, maxsize, current size
- `cache_clear()` for reset

That is a great example of honest decorator design:

- the wrapper owns policy
- the wrapper also exposes the controls needed to observe and reset that policy

That is exactly the opposite of hidden statefulness.

## The didactic comparison matters

Module 04 used a didactic cache to make state visible. This module uses `lru_cache` as
the production-grade reference point.

That comparison teaches two important habits:

- simple educational wrappers are useful when they reveal the design space
- production wrappers should not be reimplemented casually when the standard library
  already carries the hard-won semantics

That is another form of honesty: knowing when not to build your own abstraction.

## Concurrency pushes cache policy further

Even a well-designed cache becomes more expensive under concurrency:

- shared state now needs coordination
- hit and eviction logic must remain consistent
- operational hooks still need to stay safe and meaningful

The built-in `lru_cache` already handles more of this than the didactic examples earlier
in the course. That is part of why it is the right reference point here.

## Review rules for cache decorators

When reviewing a cache wrapper, keep these questions close:

- what exactly counts as the cache key?
- how does eviction work, and is it documented clearly enough?
- what hooks exist to inspect and reset cache state?
- is the wrapper reimplementing production cache behavior casually when `lru_cache` would be clearer?
- has the cache policy become significant enough that the decorator needs explicit operational surfaces?

## What to practice from this page

Try these before moving on:

1. Use `functools.lru_cache` and inspect `cache_info()` and `cache_clear()`.
2. Compare `typed=False` with `typed=True` on inputs such as `1` and `1.0`.
3. Explain one reason a hand-rolled cache decorator should stay didactic unless there is a very specific need not met by the standard tool.

If those feel ordinary, the final core can focus on the bigger design judgment: when a
wrapper should stop growing and hand policy off elsewhere.

## Continue through Module 05

- Previous: [Annotation-Aware Runtime Contracts](annotation-aware-runtime-contracts.md)
- Next: [Wrapper Policy Boundaries](wrapper-policy-boundaries.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
