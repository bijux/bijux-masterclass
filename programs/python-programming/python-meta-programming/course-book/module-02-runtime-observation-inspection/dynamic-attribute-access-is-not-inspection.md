# Dynamic Attribute Access Is Not Inspection


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Runtime Observation Inspection"]
  page["Dynamic Attribute Access Is Not Inspection"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Module 02 becomes useful the moment one sentence lands:

> reading an attribute in Python is not automatically passive.

That is why this page matters. `getattr`, `setattr`, `delattr`, and `hasattr` are not
simple dictionary helpers. They participate in the full attribute protocol and can invoke
user-defined behavior.

## The sentence to keep

When code uses dynamic attribute access, ask:

> is this trying to inspect structure, or is it intentionally participating in runtime
> behavior?

If the answer is "inspect structure," these tools are often too eager.

## These builtins are programmable dot syntax

The core builtins are close relatives of normal attribute syntax:

- `getattr(obj, name[, default])` corresponds to `obj.name`
- `setattr(obj, name, value)` corresponds to `obj.name = value`
- `delattr(obj, name)` corresponds to `del obj.name`
- `hasattr(obj, name)` effectively attempts a read and treats `AttributeError` as missing

That family resemblance is exactly why they are risky for observation. Dot syntax is not a
storage read; it is a protocol entry point.

## The attribute protocol is the real story

When you do `getattr(obj, "x")`, Python may:

- invoke `obj.__getattribute__`
- consult descriptors on the class
- consult instance storage
- fall back to class attributes
- invoke `obj.__getattr__`

Any of those steps can run user code.

The same warning applies to writes and deletes:

- `setattr` may trigger `__setattr__` or descriptor `__set__`
- `delattr` may trigger `__delattr__` or descriptor `__delete__`

## One picture of the risk

```text
getattr(obj, "x")
  -> attribute protocol
     -> __getattribute__
     -> descriptor logic
     -> __getattr__
     -> proxy or wrapper code

setattr / delattr
  -> __setattr__ / __delattr__
  -> descriptor __set__ / __delete__
```

This is why Module 02 insists that dynamic access is behavior, not neutral inspection.

## `getattr(..., default)` can hide two different situations

The optional default parameter looks convenient:

```python
value = getattr(obj, "name", None)
```

But the convenience hides an ambiguity.

The default is returned when `AttributeError` is raised, and that can mean:

- the attribute is truly missing
- the attribute exists, but its getter raised `AttributeError` internally

That ambiguity matters in real systems because it can turn internal failures into fake
"missing attribute" results.

```python
class AmbiguityDemo:
    @property
    def value(self):
        raise AttributeError("internal error")


obj = AmbiguityDemo()

try:
    getattr(obj, "value")
except AttributeError:
    print("Could be missing, or could be an internal getter failure.")
```

When the distinction matters, prefer explicit `try`/`except` around `getattr` without a
default and document what you mean by "missing."

## `hasattr` is not safe probing

`hasattr(obj, "x")` is often treated like a harmless existence check. It is not.

It attempts attribute access and only converts `AttributeError` into `False`.

That means:

- it can execute descriptors and lookup hooks
- it can hide bugs where a getter mistakenly raises `AttributeError`
- it can still let non-`AttributeError` exceptions escape

```python
class Risky:
    @property
    def x(self):
        print("property executed")
        return 1


assert hasattr(Risky(), "x") is True
```

The printed line is the lesson. The existence check already executed runtime behavior.

## `hasattr` does not swallow every failure

```python
class Explodes:
    @property
    def x(self):
        raise ValueError("boom")


# hasattr(Explodes(), "x") raises ValueError
```

This is another good reminder that `hasattr` is not separate from attribute lookup. It is
just a narrow wrapper around it.

## Dynamic mutation is still subject to object policy

Because `setattr` and `delattr` go through object policy, they are constrained by the
same runtime model as ordinary attribute syntax.

```python
class Slotted:
    __slots__ = ("x",)

    def __init__(self):
        self.x = 1


s = Slotted()
setattr(s, "x", 2)

try:
    setattr(s, "y", 3)
except AttributeError as exc:
    print("Expected:", exc)
```

The dynamic API did not bypass slots. It respected the storage and descriptor rules of
the object.

## A better helper keeps exceptions informative

When you need a helper around dynamic access, do not collapse every failure into "missing"
or "False."

For example:

```python
def try_get(obj, name):
    try:
        value = getattr(obj, name)
    except AttributeError as exc:
        return (False, exc)
    else:
        return (True, value)
```

That keeps the "attribute missing" path separate from other exceptions, which should
usually continue to surface as real failures rather than as inspection results.

## Review rules for dynamic access

When reviewing code that uses these builtins, keep these questions close:

- is the code intentionally executing the attribute protocol, or does it only need observation?
- is `hasattr` hiding a more precise question that should be asked another way?
- does `getattr(..., default)` blur together true absence and internal getter failure?
- is the code assuming `setattr` or `delattr` bypass descriptor or slot policy when they do not?
- would static lookup or direct stored-state inspection answer the real question more honestly?

## What to practice from this page

Try these before moving on:

1. Write `try_get(obj, name)` so it separates missing attributes from successful reads.
2. Build one property that raises `AttributeError` internally and explain why
   `getattr(..., default)` becomes ambiguous.
3. Show one example where `hasattr` executes code and one where it lets a non-`AttributeError`
   exception escape.

If those feel ordinary, the next step is classification: when you inspect a value, what
kind of object is it really, and how exact does your type check need to be?

## Continue through Module 02

- Previous: [Visible Names and Stored State](visible-names-and-stored-state.md)
- Next: [Exactness and Polymorphism in Runtime Type Checks](exactness-and-polymorphism-in-runtime-type-checks.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
