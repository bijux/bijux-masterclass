# Callable Objects and the Call Protocol

Once you can inspect names, state, and type relationships, another review question shows
up quickly:

> can this object be called?

Python answers that with `callable(obj)`, but the answer is narrower than many people
expect. This page makes that boundary explicit.

## The sentence to keep

When you see `callable(obj)`, ask:

> does this only mean a call attempt is supported, or is the code pretending it proves too
> much?

`callable()` is a useful gate. It is not a complete safety proof.

## What `callable(obj)` actually means

`callable(obj)` is `True` when the runtime recognizes the object as supporting call
syntax.

Common examples include:

- Python-defined functions
- built-in functions
- bound methods
- classes
- instances whose type provides `__call__`

That last phrase matters. Callability is tied to the object's type-level call protocol,
not to any random attribute named `__call__` attached later.

## `callable()` does not promise success

A `True` result does not mean:

- the arguments are valid
- the call is side-effect free
- the call is cheap
- the object is a Python-defined function

It means only that the runtime will let you attempt `obj(...)`.

That is a valuable but limited observation.

## The type provides the call protocol

This example may be surprising:

```python
class Plain:
    pass


item = Plain()
item.__call__ = lambda: 1

assert callable(item) is False
```

Why?

Because the runtime does not determine callability by looking for an instance attribute
named `__call__`. The object's type must provide the call behavior.

```python
class CallableThing:
    def __call__(self):
        return 1


obj = CallableThing()
assert callable(obj) is True
assert obj() == 1
```

This is a clean Module 02 lesson because it separates a visible attribute name from the
protocol the runtime actually uses.

## Classes are callable too

A class object is callable because calling it constructs an instance.

```python
class Service:
    pass


assert callable(Service) is True
instance = Service()
assert isinstance(instance, Service)
```

This is another reminder that callability is broader than "ordinary function."

## One picture of the observation boundary

```text
callable(obj)
  -> may I attempt obj(...)?

It does not answer:
  -> will the arguments match?
  -> will the call succeed?
  -> is this safe to execute during inspection?
```

That distinction matters in tooling, plugin discovery, and generic wrappers.

## `callable()` versus callable categories

A review often needs one more question after `callable(obj)`:

> what kind of callable is this?

The answer might be:

- function
- bound method
- class
- instance with `__call__`

That is why Module 02 keeps separating observation questions instead of treating every
"callable" as the same kind of thing. Later modules rely on those differences.

## A practical helper should keep failure information

If you want a small call guard, do not collapse everything into one boolean:

```python
def guarded_call(func, *args, **kwargs):
    if not callable(func):
        return (False, TypeError(f"{func!r} is not callable"))

    try:
        return (True, func(*args, **kwargs))
    except Exception as exc:
        return (False, exc)
```

This helper is still executing behavior when the object is callable. That is the point.
It keeps "cannot be called" separate from "can be called, but the call failed."

## Review rules for callability checks

When reviewing callability logic, keep these questions close:

- is `callable(obj)` being used only as a gate for attempted invocation, or is the code reading more into it than it should?
- does the design need to distinguish function, bound method, class, and callable instance?
- is the code assuming an instance-level `__call__` attribute makes the object callable when it does not?
- is a call attempt happening during observation when the tool should have remained non-executing?
- are call failures kept distinct from non-callable inputs?

## What to practice from this page

Try these before moving on:

1. Build one class whose instances become callable through a type-level `__call__`.
2. Add a `__call__` attribute directly to one instance and explain why `callable(obj)` stays false.
3. Write `guarded_call(f, *args, **kwargs)` and keep non-callable inputs separate from
   callable-but-failing ones.

If those feel ordinary, the last core can connect the whole module into one disciplined
observation workflow with static lookup.

## Continue through Module 02

- Previous: [Exactness and Polymorphism in Runtime Type Checks](exactness-and-polymorphism-in-runtime-type-checks.md)
- Next: [Static Lookup and Disciplined Observation](static-lookup-and-disciplined-observation.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
