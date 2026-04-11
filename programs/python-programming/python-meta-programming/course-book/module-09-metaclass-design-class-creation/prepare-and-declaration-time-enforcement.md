# `__prepare__` and Declaration-Time Enforcement

This core covers the one metaclass hook that feels unusual for a very good reason:

it can act before the class body has finished executing.

That makes it unique in the whole class-creation pipeline.

## The sentence to keep

`__prepare__` is the only metaclass hook that can supply the namespace mapping used during
class body execution, which makes it the only place where declaration-time assignment rules
can be enforced directly.

That is why it exists.

## Why `__prepare__` is different

Most metaclass hooks see the class only after the body has already executed or after the
class object has already been created.

`__prepare__` is different because it decides:

- what mapping receives class-body assignments
- what behavior that mapping has while assignments happen

That means it can observe or reject things that later hooks can only discover after the
fact.

## A compact mental model

```text
metaclass resolution
  -> __prepare__ creates namespace mapping
  -> class body writes into that mapping
  -> __new__ receives the finished namespace
```

This is the real reason `__prepare__` matters.

## A duplicate-assignment example

```python
class NoDupesMeta(type):
    class NoDupesDict(dict):
        def __setitem__(self, key, value):
            is_dunder = key.startswith("__") and key.endswith("__")
            if key in self and not is_dunder:
                raise ValueError(f"duplicate assignment to {key!r}")
            super().__setitem__(key, value)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return NoDupesMeta.NoDupesDict()


class OK(metaclass=NoDupesMeta):
    x = 1
    y = 2
```

This works because the class body is writing into a custom mapping, not into an ordinary
plain dictionary.

## What later hooks cannot do as cleanly

Suppose the class body assigns:

```python
x = 1
x = 2
```

By the time `__new__` sees the namespace, only the final value remains unless the mapping
has already recorded the duplicate event.

That is the heart of declaration-time enforcement:

some facts exist only while the class body is still running.

## What custom namespace mappings can enforce

With care, a `__prepare__` mapping can do things like:

- reject duplicate assignments
- record declaration order
- capture extra metadata during assignment
- trace or audit what the class body writes

Those are all genuinely different from post-hoc validation.

## Why this hook should still stay narrow

`__prepare__` is powerful, but it is also easy to overuse.

If the rule can be checked after class creation just as clearly, then a custom namespace
mapping may be unnecessary.

The honest use case is:

- this fact matters specifically during declaration
- and it cannot be reconstructed cleanly later

That keeps the hook justified.

## A declaration-order sketch

Another classic use is to keep assignment order visible:

```python
class TracingMeta(type):
    class TrackingDict(dict):
        def __init__(self):
            super().__init__()
            self.order = []

        def __setitem__(self, key, value):
            self.order.append(key)
            super().__setitem__(key, value)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return TracingMeta.TrackingDict()
```

This is a good reminder that `__prepare__` is about the namespace mapping itself, not only
about metaclass validation.

## Why modern ordered dict behavior does not remove the lesson

Modern Python preserves class-body definition order in ordinary dictionaries, which is very
useful.

But `__prepare__` still matters because:

- it can enforce rules during assignment
- it can capture richer metadata than final order alone
- it can expose behaviors ordinary dictionaries do not provide

So the point of the hook is not “ordered class dictionaries exist.” The point is control
over declaration-time semantics.

## What this core makes clear

The point is not “always customize the class namespace.”

The boundary is:

- there is one hook that can see class-body writes as they happen
- that hook exists for declaration-time rules
- if you use it, you should be able to name exactly what later hooks would miss

That is the discipline Module 09 wants.

## Review rules for `__prepare__`

When reviewing a metaclass that uses `__prepare__`, keep these questions close:

- what class-body fact is being captured or enforced during assignment?
- could the same rule be checked just as clearly in `__new__` instead?
- is the custom mapping small and inspectable?
- does the mapping preserve the behaviors the rest of the class body expects?
- is the design using `__prepare__` because it is necessary, or just because it is exotic?

## What to practice from this page

Try these before moving on:

1. Build one custom mapping that rejects duplicate non-dunder assignments.
2. Build one mapping that records definition order and stores it on the class later.
3. Write one short review note explaining why a proposed `__prepare__` hook is unnecessary because later validation would be just as clear.

If those feel ordinary, the next step is the module's design page: when metaclass power is
truly justified and when lower-power tools should still win.

## Continue through Module 09

- Previous: [Metaclass `__new__` and `__init__`](metaclass-new-and-init.md)
- Next: [Metaclass Boundaries and Class-Creation Ownership](metaclass-boundaries-and-class-creation-ownership.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
