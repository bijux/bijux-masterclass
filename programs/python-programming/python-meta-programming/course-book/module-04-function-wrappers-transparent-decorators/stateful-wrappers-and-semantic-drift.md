# Stateful Wrappers and Semantic Drift

Module 04 needs one explicit warning boundary:

> the moment a decorator starts keeping state across calls, it stops being "just a thin
> wrapper" and starts owning policy.

That does not make stateful decorators forbidden. It makes them more expensive to review,
test, and reason about.

## The sentence to keep

When a wrapper stores state, ask:

> what semantic rule does this state now own across calls?

That is the right review question because state changes behavior over time, not only at
one call boundary.

## `@once` is the simplest stateful example

```python
import functools


def once(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "_once_result"):
            wrapper._once_result = func(*args, **kwargs)
        return wrapper._once_result

    return wrapper
```

This looks small, but the semantics are no longer thin:

- the first successful call determines future results
- later arguments are ignored
- wrapper state changes what the function now means

That is a policy surface, even though the syntax is still tiny.

## State changes the review cost

A stateful wrapper raises new questions that thin wrappers often avoid:

- where is the state stored?
- when is it initialized?
- when is it reset?
- what happens if the first call raises?
- what happens under concurrency?

These are not side questions. They are part of the wrapper's real semantics.

## Order sensitivity becomes more important with state

Stacked stateful decorators are especially sensitive to order.

For example:

- `@once @timer` means the timer only matters on the first successful call
- `@timer @once` means timing logic still runs on every outer call, even if the inner once-wrapper returns a cached result

That is why decorator order is never just formatting.

## One picture of semantic drift

```text
Thin wrapper:
  same call -> same semantics, plus narrow observation or signaling

Stateful wrapper:
  same call -> behavior may now depend on prior calls, cached values, counters, or history
```

That difference is the whole reason this page exists.

## State can live in a closure or on the wrapper object

Two common storage patterns are:

- closure-held state with `nonlocal`
- wrapper attributes such as `wrapper._once_result`

Both are real runtime state. The right question is not which one looks cleaner. It is:

> which one makes the behavior, reset path, and inspection story clearer?

State stored on the wrapper object is often easier to inspect and reset deliberately,
which matters a lot in tests and long-running processes.

## Failure behavior is part of the policy

A stateful decorator must make failure semantics explicit.

For `@once`, a serious review question is:

- if the first call raises, is the failed result cached or not?

A small implementation detail can change this completely.

That is why stateful decorators deserve slower, more honest review than thin wrappers.

## Concurrency is not an afterthought

The moment wrapper state can be touched by multiple threads or tasks, the design cost goes
up again.

Even a tiny stateful decorator can become wrong under concurrency if it assumes a
single-threaded world.

This module does not need to solve every concurrency case. It does need to name the
boundary clearly:

- stateful wrappers are more than syntactic sugar
- they are small runtime systems

## Stateful wrappers may deserve explicit reset hooks

If a wrapper owns meaningful state, the design may need an explicit hook such as:

- `cache_clear()`
- reset methods for tests
- visible attributes for debugging

That is one reason the worked example uses a didactic cache with explicit state surfaces
instead of hiding everything behind one opaque closure.

## Review rules for stateful wrappers

When reviewing a stateful decorator, keep these questions close:

- what semantic rule does the state now control across calls?
- where does the state live, and how visible is it to tests and debugging?
- what happens on the first failure or partial success?
- how does decorator order change the resulting semantics?
- is this still the smallest honest tool, or has the decorator become a small framework?

## What to practice from this page

Try these before moving on:

1. Implement `@once` and explain exactly what later calls do with new arguments.
2. Stack `@once` with a thin timing decorator in both orders and compare the behavior.
3. Write down one stateful decorator idea that should probably become an explicit object instead of another wrapper.

If those feel ordinary, the next step is to keep wrapped callables honest to tools and
reviewers with `functools.wraps`.
