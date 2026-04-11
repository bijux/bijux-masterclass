# Descriptor Protocol and `__set_name__`

Module 07 starts by making one thing explicit:

attribute access is a protocol surface, not just a dictionary lookup.

Descriptors are a big part of that protocol.

## The sentence to keep

A descriptor is any object stored on a class that defines `__get__`, `__set__`, or
`__delete__`, and Python consults those hooks during attribute access instead of always
returning the raw class attribute.

That is the foundation the rest of the module depends on.

## The four hooks in one place

The full descriptor surface for this module is:

- `__get__(self, obj, owner=None)` for reads
- `__set__(self, obj, value)` for writes
- `__delete__(self, obj)` for deletes
- `__set_name__(self, owner, name)` for class-creation-time self-configuration

Only the first three participate in making an object a descriptor.

`__set_name__` matters because reusable descriptors often need to learn:

- the owning class
- the public attribute name
- the private storage name they should use internally

## What each hook is really for

Keep the jobs separate:

- `__get__` decides what `obj.attr` or `Cls.attr` should return
- `__set__` decides what happens when code assigns `obj.attr = value`
- `__delete__` decides what `del obj.attr` means
- `__set_name__` lets the descriptor configure itself once when the class is created

That separation matters because many production descriptors use only two or three of these
hooks, not all four.

## A small but important clarification

`__set_name__` alone does not make something a descriptor.

This object:

```python
class NameAwareOnly:
    def __set_name__(self, owner, name):
        self.name = name
```

is name-aware, but it is not a descriptor until it also defines `__get__`, `__set__`, or
`__delete__`.

That distinction prevents a lot of fuzzy explanations later.

## The default pipeline still begins with `__getattribute__`

Even though Module 07 is about descriptors, instance lookup still begins here:

```python
obj.__getattribute__("attr")
```

The key point is that `object.__getattribute__` applies descriptor rules as part of the
default lookup pipeline.

So the useful mental model is:

```text
attribute access
  -> default __getattribute__
  -> descriptor / instance dictionary / class lookup rules
```

Later modules may discuss overrides of `__getattribute__`, but here the goal is to master
the default behavior first.

## A compact descriptor example

```python
class IntegerField:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private_name, 0)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.public_name} must be an int")
        obj.__dict__[self.private_name] = value


class Counter:
    count = IntegerField()


c = Counter()
c.count = 3
print(c.count)  # 3
```

This example is small, but it already shows the module's main mechanics:

- class-level installation
- name learning through `__set_name__`
- per-instance storage in `obj.__dict__`
- validation at the attribute boundary

## Why class access usually returns the descriptor itself

A common convention is:

```python
if obj is None:
    return self
```

inside `__get__`.

That makes class access such as `Counter.count` return the descriptor object itself so
review, debugging, and introspection can still see the configured field owner.

It is not the only possible design, but it is the standard one and the clearest default.

## Which hooks matter most in practice

The hooks are not equally common:

- `__get__` appears in almost every useful descriptor
- `__set__` is common for validators, coercion, and field systems
- `__set_name__` is very common in modern reusable descriptors
- `__delete__` is comparatively rare

That matters because beginners sometimes assume a descriptor is incomplete unless it
implements every hook. It is not.

## What not to do with descriptor state

One of the earliest descriptor mistakes is storing per-instance values on the descriptor
object itself.

That is wrong because the descriptor instance usually lives on the class and is shared by
every object of that class.

Bad pattern:

```python
class BrokenField:
    def __init__(self):
        self.value = None
```

That shape almost always means instance state will leak across objects.

Module 07 will come back to storage patterns in detail, but the rule starts here:

store per-instance state on the instance or in safe external storage, not on the
descriptor itself.

## Review rules for the protocol

When reviewing descriptor code, keep these questions close:

- which of the protocol hooks are actually implemented?
- does the code know that `__set_name__` is supportive, not sufficient?
- where does per-instance state live?
- what happens on class access when `obj is None`?
- is this really attribute-boundary behavior, or is a simpler method or property enough?

## What to practice from this page

Try these before moving on:

1. Write one descriptor that only defines `__get__` and explain why it is still a descriptor.
2. Add `__set_name__` to a reusable field and show how it removes hard-coded attribute names.
3. Inspect one class access such as `MyClass.field` and explain why returning the descriptor object is useful.

If those feel ordinary, the next step is precedence: why some descriptors beat instance
state while others can be shadowed.

## Continue through Module 07

- Previous: [Overview](index.md)
- Next: [Data and Non-Data Descriptor Precedence](data-and-non-data-descriptor-precedence.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
