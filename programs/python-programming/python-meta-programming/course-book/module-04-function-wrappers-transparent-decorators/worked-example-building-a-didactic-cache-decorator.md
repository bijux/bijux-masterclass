# Worked Example: Building a Didactic Cache Decorator

The five core lessons in Module 04 become much easier to trust when they all show up in
one wrapper that is useful, tempting, and clearly not production-ready.

A small cache decorator is perfect for that job because it sits right on the boundary
between:

- thin wrapper mechanics
- stateful semantic drift
- metadata preservation
- explicit policy and reset needs

That makes it the right worked example for this module.

## The incident

Assume a team wants a teaching cache decorator for small demos and local experiments.

The decorator should:

- cache results by arguments
- expose visible state for inspection and reset
- preserve function identity for tools
- stay honest about its limitations

That last goal matters most. This is where many wrappers go wrong: they look tiny and end
up behaving like unreviewed framework features.

## The design boundary

This worked example is deliberately didactic, not production-grade.

That means the design will:

- preserve metadata with `functools.wraps`
- expose `cache_clear()` for explicit reset
- keep cache state on the wrapper for visibility
- remain single-threaded and intentionally limited

Those choices are not accidental. They make the wrapper more inspectable and easier to
review as a teaching artifact.

## Step 1: make the decorator factory timing explicit

The cache uses a factory so configuration happens once at definition time:

```python
@cache(maxsize=3)
def fib(n):
    ...
```

This means:

1. `cache(maxsize=3)` runs once
2. it returns the real decorator
3. that decorator wraps `fib`

That definition-time sequence matters because `maxsize` is configuration, not per-call
input.

## Step 2: admit that caching is stateful policy

Caching is not a thin wrapper. It changes semantics across calls:

- later calls may skip execution
- result meaning now depends on wrapper state
- argument keying rules affect correctness
- reset behavior matters to tests and long-running processes

That is why this worked example belongs after the stateful-wrapper core, not inside the
thin-wrapper page.

## Step 3: preserve metadata and expose state deliberately

The wrapper should keep the original function inspectable:

- use `functools.wraps`
- store state on explicit wrapper attributes
- expose a `cache_clear()` hook

That combination gives both transparency and testability.

## A didactic implementation

```python
import functools
from typing import Any, Callable, Dict, Hashable, Optional


def cache(maxsize: Optional[int] = 128) -> Callable:
    if maxsize is not None and maxsize < 0:
        raise ValueError("maxsize must be >= 0 or None")

    if maxsize == 0:
        def decorator_no_cache(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                return func(*args, **kwargs)

            def cache_clear() -> None:
                pass

            wrapper.cache_clear = cache_clear
            return wrapper

        return decorator_no_cache

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                key: Hashable = (args, frozenset(kwargs.items()))
            except TypeError as exc:
                raise TypeError(
                    "cache() only supports hashable arguments in its canonical form"
                ) from exc

            if key in wrapper._cache:
                wrapper._cache_order.remove(key)
                wrapper._cache_order.append(key)
                return wrapper._cache[key]

            result = func(*args, **kwargs)

            if maxsize is not None and len(wrapper._cache_order) >= maxsize:
                oldest = wrapper._cache_order.pop(0)
                del wrapper._cache[oldest]

            wrapper._cache[key] = result
            wrapper._cache_order.append(key)
            return result

        wrapper._cache: Dict[Hashable, Any] = {}
        wrapper._cache_order: list = []

        def cache_clear() -> None:
            wrapper._cache.clear()
            wrapper._cache_order.clear()

        wrapper.cache_clear = cache_clear
        return wrapper

    return decorator
```

## Why this version is useful as a teaching artifact

This cache is intentionally not pretending to be perfect.

It is useful because it makes the right tradeoffs visible:

- `wraps` keeps the callable inspectable
- wrapper attributes make state explicit
- `cache_clear()` makes reset behavior explicit
- the hashability rule is named rather than hidden
- capacity and eviction behavior are reviewable in code

That transparency is more important here than raw cleverness.

## The limitations are part of the lesson

This decorator is didactic because it leaves real limitations visible:

- it is not concurrency-safe
- it uses a simple O(n) eviction path
- it requires hashable arguments in its canonical key form
- it is not a substitute for `functools.lru_cache`

Those limitations are not embarrassing leftovers. They are the proof that the wrapper is
being taught honestly.

## Order and policy still matter

If you stack this cache with other decorators, semantics change:

- logging outside the cache logs every call attempt
- logging inside the cache logs only cache misses
- timing outside the cache times both hits and misses
- timing inside the cache mostly times uncached work

That reinforces the module's central point: stacked decorator order is semantic, not
ornamental.

## What this example teaches about Module 04

This worked example ties the module together:

- nested wrappers and rebinding mechanics still underlie the design
- definition-time factory behavior stays separate from call-time cache behavior
- stateful wrappers deserve policy-level review
- `functools.wraps` and explicit state surfaces keep the wrapper inspectable

That is the real lesson. The cache is not here as a production recommendation. It is here
as a clear specimen of where transparency starts to give way to policy.

## The review loop to keep

When you inherit or design a stateful decorator, run this loop:

1. identify the state and the semantic rule it now owns
2. make reset and inspection surfaces explicit
3. preserve metadata so tooling can still see the logical callable
4. document limitations instead of letting the wrapper pretend to be more general than it is

If you can do that here, Module 04 has done its job and the next decorator module can take
on heavier policy and typing concerns with less ambiguity.
