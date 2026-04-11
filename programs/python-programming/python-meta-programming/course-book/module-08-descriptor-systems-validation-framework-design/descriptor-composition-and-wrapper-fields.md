# Descriptor Composition and Wrapper Fields

Once descriptor systems start carrying several concerns at once, teams hit a design fork:

- create more subclasses for every combination
- or layer behavior around an inner field

This core focuses on the second option.

## The sentence to keep

Descriptor composition wraps one field descriptor in another so new behavior can be added
through delegation instead of by multiplying subclasses for every field variant.

That is useful, but only if the layers stay inspectable.

## Why composition shows up here

By Module 08, a field might want more than one concern:

- storage
- validation
- coercion
- logging
- caching

If every combination becomes its own subclass, the design quickly turns into a class tree
that is harder to review than the field logic itself.

Composition is the usual escape hatch.

## A delegation base

```python
class FieldWrapper:
    def __init__(self, inner):
        self.inner = inner

    def __set_name__(self, owner, name):
        self.inner.__set_name__(owner, name)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return self.inner.__get__(obj, owner)

    def __set__(self, obj, value):
        self.inner.__set__(obj, value)
```

This is the useful center of the pattern:

- the wrapper owns one extra concern
- the inner descriptor still owns the underlying field contract

That keeps layering explicit.

## A validated wrapper

```python
def validated(validator, inner):
    class ValidatedField(FieldWrapper):
        def __init__(self):
            super().__init__(inner)

        def __set__(self, obj, value):
            self.inner.__set__(obj, validator(value))

    return ValidatedField()
```

This shape works because the wrapper does one narrow thing:

- it transforms or rejects the incoming value
- then it delegates ordinary field storage to the inner descriptor

That is much easier to reason about than a whole new subclass hierarchy for every rule.

## What good composition looks like

Good wrapper-field composition usually has these traits:

- one obvious inner owner
- one obvious added concern per layer
- consistent forwarding of `__set_name__`, `__get__`, and `__set__`
- shallow enough depth that a reviewer can still follow it mentally

That last point matters more than people think.

## What bad composition looks like

Composition becomes harder to trust when:

- wrappers hide the inner descriptor completely
- different layers each mutate values in surprising ways
- `__set_name__` is forwarded inconsistently
- the stack grows deep enough that field behavior becomes an archaeological dig

At that point, “composable” is no longer the same as “clear.”

## Why `__set_name__` deserves special care

One easy bug in wrapped descriptors is forwarding `__set_name__` incorrectly.

Problems include:

- never forwarding it to the inner field
- forwarding it more than once
- partially shadowing the name state in both wrapper and inner descriptor

Because `__set_name__` often initializes storage keys and public names, this is not a
small detail. It is part of whether the wrapped field works at all.

## Composition is not a license for endless stacks

There is a real limit to how many field layers remain readable.

As a practical rule, very shallow composition is much easier to justify than deep stacks.

If a field design now wants:

- logging
- validation
- coercion
- caching
- encryption
- remote persistence

all as separate wrapper layers, the design may already be asking for a stronger framework
abstraction than “one wrapped descriptor.”

## Why this is better than subclass explosion

Used well, composition lets a field system say:

- here is the base storage or coercion field
- here is one wrapper adding validation
- here is another wrapper adding one more cross-cutting concern

That makes behavior additive and local instead of forcing a huge family of subclasses such
as:

- `CachedStringField`
- `ValidatedCachedStringField`
- `LoggedValidatedCachedStringField`

and so on.

The goal is not sophistication. The goal is keeping ownership legible.

## Review rules for wrapper fields

When reviewing descriptor composition, keep these questions close:

- what does the inner descriptor own?
- what one extra concern does this wrapper add?
- is `__set_name__` delegated correctly and only once?
- how many layers does a reader need to traverse to understand one attribute write?
- has the stack grown large enough that a different framework abstraction would be clearer?

## What to practice from this page

Try these before moving on:

1. Wrap one validating field around one storage field and explain which concern each layer owns.
2. Show one bug caused by forgetting to forward `__set_name__`.
3. Write one short review note rejecting a four-layer field stack as too opaque.

If those feel ordinary, the next step is hint-driven validation and coercion, where the
descriptor starts reading type metadata as runtime evidence.
