# Metaclass Resolution, Timing, and Conflicts

Once you know that class creation is a runtime event, the next question is:

which metaclass actually controls that event?

This core answers that question and makes one practical consequence unavoidable:

metaclass work runs at definition time, which usually means import time.

## The sentence to keep

Python resolves one effective metaclass for the class being created, runs its class
creation logic at definition time, and raises conflicts when multiple inheritance brings
incompatible metaclass owners together.

That one sentence explains most “why did this metaclass run?” questions.

## Timing comes first

Before talking about conflict rules, keep the timing clear:

metaclass work runs when the class is defined, not when instances are created.

In ordinary code that usually means:

- module import time
- class statement execution time

That matters because any heavy work, I/O, or global mutation performed by a metaclass now
happens before objects are ever instantiated.

## Where the effective metaclass comes from

There are two broad routes:

- an explicit `metaclass=...` on the class statement
- an implicit metaclass derived from the base classes

Python then needs one effective metaclass that is compatible with the bases involved.

That is why metaclass selection is not only a syntax detail. It is a multiple-inheritance
rule.

## A compact mental model

```text
explicit metaclass, if present
  -> must be compatible with the metaclasses of the bases

no explicit metaclass
  -> Python derives the effective metaclass from the bases

no compatible common metaclass
  -> metaclass conflict
```

That is the review-level model most people need.

## A small metaclass example

```python
class TaggedMeta(type):
    def __new__(mcs, name, bases, namespace):
        namespace["tag"] = f"created by {mcs.__name__}"
        return super().__new__(mcs, name, bases, namespace)


class Base(metaclass=TaggedMeta):
    pass


class Child(Base):
    pass


print(Base.tag)   # created by TaggedMeta
print(Child.tag)  # created by TaggedMeta
```

This example shows two useful facts:

- metaclass effects are inherited through the class hierarchy
- subclasses often keep the same metaclass implicitly

That “infectious” behavior is exactly why metaclasses need stronger review discipline.

## Why conflicts happen

Conflicts appear when multiple bases carry metaclasses that do not fit into one compatible
hierarchy.

For example:

```python
class MetaA(type):
    pass


class MetaB(type):
    pass


class A(metaclass=MetaA):
    pass


class B(metaclass=MetaB):
    pass


try:
    class Bad(A, B):
        pass
except TypeError as exc:
    print("Expected:", exc)
```

The conflict is not Python being fussy. It is Python telling you that two different
class-creation owners are being combined without one clear higher-level owner.

## Why “just combine them” is not always the answer

You can sometimes write a joint metaclass:

```python
class MetaAB(MetaA, MetaB):
    pass
```

But this is only safe when the underlying behaviors truly compose.

That means a joint metaclass is:

- a semantic design decision
- not a mechanical repair step

If the two metaclasses want incompatible timing, validation, or registration behavior, a
joint metaclass may make the code worse rather than better.

## Import-time effects are part of the design

Because resolution happens at definition time, every metaclass decision also carries an
import-time design choice.

Questions that matter immediately include:

- does this metaclass mutate global registries?
- does it do expensive scanning or I/O?
- does class definition order now affect behavior?

If those questions are not answered, the metaclass is not yet review-ready.

## What this core is really trying to teach

The point is not merely to memorize conflict errors.

The point is to understand that metaclasses are:

- inherited
- definition-time
- hierarchy-shaping

Those three facts are enough to explain most of their risk surface.

## Review rules for resolution and conflicts

When reviewing metaclass selection, keep these questions close:

- where is the effective metaclass coming from?
- what work does it do at class-definition time?
- are multiple bases introducing incompatible metaclass owners?
- if a joint metaclass is proposed, do the underlying behaviors really compose?
- would a lower-power tool avoid the import-time and inheritance consequences entirely?

## What to practice from this page

Try these before moving on:

1. Build one tiny metaclass that adds a marker attribute and show that subclasses inherit the metaclass implicitly.
2. Trigger one metaclass conflict on purpose and explain it in ownership language instead of only error-message language.
3. Write one short review note rejecting a “just combine the metaclasses” fix as semantically unsafe.

If those feel ordinary, the next step is to separate structural work in metaclass
`__new__` from post-creation bookkeeping in metaclass `__init__`.
