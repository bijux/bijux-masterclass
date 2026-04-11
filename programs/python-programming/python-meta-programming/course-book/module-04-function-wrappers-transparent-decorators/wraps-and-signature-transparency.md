# Wraps and Signature Transparency

By the time Module 04 reaches this page, one rule should feel non-negotiable:

> if a decorator is meant to stay transparent, it must preserve callable identity and
> inspection surfaces honestly.

That is why `functools.wraps` is not a style flourish. It is part of correctness.

## The sentence to keep

When reviewing a decorator, ask:

> after wrapping, what will tools and reviewers now see when they inspect this callable?

If the answer is "just `wrapper(*args, **kwargs)` and a lost docstring," the decorator has
already damaged transparency.

## What bare wrappers lose

Without preservation, a wrapped callable often exposes the wrapper's identity instead of
the original callable's identity:

- `__name__` becomes `"wrapper"`
- `__doc__` may disappear
- annotations may disappear
- signature reporting may degrade to `(*args, **kwargs)`
- unwrapping tools lose the original function path

That is real breakage for:

- `inspect.signature`
- documentation tooling
- debuggers
- stack traces
- reviewers trying to understand what was wrapped

## `functools.wraps` restores the important metadata

`functools.wraps(wrapped)` is the standard way to preserve the original callable's visible
identity on the wrapper.

In practice, it copies or updates metadata such as:

- `__module__`
- `__name__`
- `__qualname__`
- `__doc__`
- `__annotations__`
- `__dict__`

and, importantly, sets:

- `__wrapped__`

That `__wrapped__` chain is what lets inspection tools recover the logical callable under
the wrapper.

## Bare versus preserved wrapping

```python
import functools
import inspect


def bare_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def preserved_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@bare_decorator
def bare_func(x):
    """Bare doc."""
    return x


@preserved_decorator
def preserved_func(x):
    """Preserved doc."""
    return x


print(bare_func.__name__)
print(preserved_func.__name__)
print(inspect.signature(bare_func))
print(inspect.signature(preserved_func))
```

That contrast is the entire lesson:

- the bare wrapper changes what tools see
- the preserved wrapper keeps the original callable legible

## One picture of preserved transparency

```text
Without wraps:
  wrapped function -> visible as generic wrapper

With wraps:
  wrapped function -> visible as original name/doc/annotations
  plus __wrapped__ -> original callable for unwrapping and signature recovery
```

This is why `wraps` belongs in the definition-time part of the decorator, not as an
optional cleanup later.

## `__wrapped__` is especially important

The copied name and docstring are helpful. The `__wrapped__` chain is what keeps later
inspection honest.

It supports tools that need to:

- recover signatures
- unwrap stacked decorators
- document the original callable
- reason about what was transformed

That makes `__wrapped__` a practical inspection surface, not an obscure implementation
detail.

## Custom preservation is possible, but the standard tool should be the default

You can write your own metadata-preservation helper. In rare cases, you may need custom
control.

But the right default is still:

```python
@functools.wraps(func)
def wrapper(*args, **kwargs):
    ...
```

That default is simple, well understood, and aligned with Python's introspection tools.

If a custom helper is used, the review burden goes up because the team now has to verify
that the custom preservation is truly equivalent where it matters.

## Signature transparency matters to later modules

This page also closes the loop with Module 03:

- signatures are strong runtime evidence
- decorators can damage that evidence
- `wraps` helps preserve the evidence path by keeping `__wrapped__` intact

That is why the course teaches `functools.wraps` before heavier decorator policy. If
transparency is weak here, everything built on inspection later becomes less trustworthy.

## Review rules for transparency preservation

When reviewing a decorator, keep these questions close:

- does the wrapper use `functools.wraps` by default?
- what metadata will callers and tools see after wrapping?
- is `__wrapped__` preserved so unwrapping and signature recovery still work?
- has the decorator changed the callable contract in ways `wraps` alone cannot repair?
- if a custom preservation helper exists, is there a real reason not to use the standard tool?

## What to practice from this page

Try these before moving on:

1. Compare a bare wrapper with a `functools.wraps`-based wrapper using `__name__`, `__doc__`, and `inspect.signature`.
2. Use `inspect.unwrap` or `__wrapped__` to trace one decorated function back to its original callable.
3. Write down one reason `functools.wraps` is part of correctness and not only style.

If those feel ordinary, the worked example can stress-test transparency and state together
inside a deliberately limited cache decorator.

## Continue through Module 04

- Previous: [Stateful Wrappers and Semantic Drift](stateful-wrappers-and-semantic-drift.md)
- Next: [Worked Example: Building a Bounded Cache Decorator](worked-example-building-a-bounded-cache-decorator.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
