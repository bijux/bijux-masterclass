# Reusable Field Descriptors and Storage

This core moves from understanding descriptor mechanics to using them as a repeatable
design tool.

The moment descriptors become truly useful is when one field rule needs to be reused
across many attributes or classes.

## The sentence to keep

A reusable field descriptor is usually a data descriptor that learns its public name with
`__set_name__`, validates or coerces values in `__set__`, and keeps per-instance state out
of the descriptor object itself.

That last part is the one that prevents the most bugs.

## What a reusable field descriptor usually owns

In this module, a field descriptor is a small class that:

- takes configuration in `__init__`
- learns its installed attribute name in `__set_name__`
- intercepts reads and writes through `__get__` and `__set__`
- stores per-instance values in a safe place

That pattern is what turns descriptor protocol knowledge into something practical.

## A small string field

```python
class StringField:
    def __init__(self, max_length=None):
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private_name, "")

    def __set__(self, obj, value):
        text = str(value)
        if self.max_length is not None and len(text) > self.max_length:
            raise ValueError(f"{self.public_name} exceeds {self.max_length} characters")
        obj.__dict__[self.private_name] = text
```

This is the standard educational shape because every important part stays visible.

## A positive integer field

```python
class PositiveInt:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private_name, 0)

    def __set__(self, obj, value):
        number = int(value)
        if number < 0:
            raise ValueError(f"{self.public_name} must be non-negative")
        obj.__dict__[self.private_name] = number
```

This is where descriptors clearly outgrow a single property:

- the rule is reusable
- the attribute name is discovered automatically
- the field behavior is declarative at class definition time

## The storage rule that matters most

The descriptor object usually lives once on the class.

So this is a bug:

```python
class BrokenField:
    def __init__(self):
        self.value = None

    def __get__(self, obj, owner=None):
        return self.value

    def __set__(self, obj, value):
        self.value = value
```

Every instance will share the same `self.value` because that state lives on the descriptor
object itself.

The safer pattern is:

```python
obj.__dict__[self.private_name] = value
```

or explicit external storage when `__dict__` is not available.

## Slotted classes need a different storage owner

If a class uses `__slots__` and does not expose `__dict__`, ordinary instance-dictionary
storage is unavailable.

That is where external storage patterns become useful.

One common teaching pattern is `WeakKeyDictionary`:

```python
from weakref import WeakKeyDictionary


class SlottedPositiveInt:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self._values.get(obj, 0)

    def __set__(self, obj, value):
        number = int(value)
        if number < 0:
            raise ValueError("value must be non-negative")
        self._values[obj] = number
```

This pattern keeps per-instance values separate while still allowing instances to be
garbage-collected.

## Why `id(obj)` storage is a trap

Sometimes people try:

```python
storage[id(obj)] = value
```

That is a poor storage design because object ids can be reused after garbage collection,
and the mapping can easily leak stale state.

If external storage is needed, weak references are the safer direction.

## What reusable field descriptors are good at

Use them when:

- the same field rule repeats across many classes
- the rule truly belongs to assignment or access of that attribute
- class-level declaration makes the model easier to read

That is where descriptors start earning their complexity.

## What they are not automatically good at

Descriptors are not automatically the right fit for:

- one one-off field rule on one class
- wide object-level invariants spanning many attributes
- full validation frameworks with cross-field coordination

Those cases may still belong to properties, explicit validators, or later-course
architectures.

## A compact review checklist

When reviewing reusable field descriptors, ask:

- is the rule reusable enough to justify a descriptor?
- where does per-instance state live?
- is `__set_name__` removing hard-coded attribute names?
- does the descriptor clearly separate configuration from stored values?
- would one property still be clearer if the reuse pressure is low?

## What to practice from this page

Try these before moving on:

1. Build one reusable validating field and install it on two attributes with different names.
2. Demonstrate the shared-state bug caused by storing values on the descriptor itself.
3. Sketch a slotted-compatible version and explain why weak-reference storage is safer than `id(obj)` storage.

If those feel ordinary, the next step is the design boundary page: when descriptor power
is truly the right owner and when it is more than the problem needs.

## Continue through Module 07

- Previous: [Functions, Binding, and Method Descriptors](functions-binding-and-method-descriptors.md)
- Next: [Descriptor Boundaries and Attribute Ownership](descriptor-boundaries-and-attribute-ownership.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
