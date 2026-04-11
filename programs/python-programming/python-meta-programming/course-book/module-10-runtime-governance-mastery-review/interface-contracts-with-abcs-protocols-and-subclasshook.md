# Interface Contracts with ABCs, Protocols, and `__subclasshook__`

Once dynamic execution boundaries are clear, the next governance question is smaller but
equally important:

what does a runtime "interface" actually promise?

Python gives several ways to name an interface, but those ways do not all guarantee the
same thing.

## The sentence to keep

ABCs, protocols, and `__subclasshook__` are useful only when the code review story stays
honest about whether the contract is nominal, structural, static, shallow, or truly
behavioral.

That sentence is the whole page in miniature.

## ABCs name a runtime contract with real but narrow force

`abc.ABC` plus `@abstractmethod` can prevent instantiation of incomplete subclasses.

That is a real runtime guardrail:

```python
from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        ...


class Circle(Drawable):
    def draw(self) -> str:
        return "circle"


print(Circle().draw())  # circle
```

And the failure mode is precise too:

```python
try:
    Drawable()
except TypeError as exc:
    print("expected:", exc)
```

This is useful, but it is not a full semantic proof. An ABC can require the presence of a
method. It does not guarantee the method behaves well.

## Protocols are primarily for static structural typing

`typing.Protocol` shines when you want structural compatibility checked by type checkers.

That is the key idea to keep. Runtime use is secondary.

```python
from typing import Protocol


class SupportsClose(Protocol):
    def close(self) -> None:
        ...
```

This says "objects with a compatible `close()` method fit this contract" for static
analysis. That is valuable because it keeps interfaces flexible without forcing
inheritance.

The governance trap is pretending that a protocol automatically proves runtime behavior.
It does not.

## `@runtime_checkable` is shallow on purpose

Protocols can opt into runtime checks:

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> None:
        ...


class FileLike:
    def close(self) -> None:
        print("closed")


print(isinstance(FileLike(), SupportsClose))  # True
print(isinstance(123, SupportsClose))         # False
```

That can be useful at API boundaries, but the check stays shallow:

- it does not prove semantic invariants
- it does not deeply validate signatures the way reviewers often imagine
- it does not replace real tests

In other words, runtime-checkable protocols are for light structural filtering, not for
strong runtime certification.

## `__subclasshook__` should stay boring

An abstract base class can declare virtual subclassing rules with `__subclasshook__`.

```python
from abc import ABC


class HasLen(ABC):
    @classmethod
    def __subclasshook__(cls, candidate):
        if hasattr(candidate, "__len__") and callable(getattr(candidate, "__len__", None)):
            return True
        return NotImplemented
```

That hook is defensible only when it stays simple enough to inspect quickly.

Strong uses usually look like:

- a small attribute presence check
- maybe one callable check
- `NotImplemented` for everything else

Weak uses try to smuggle business meaning into a structural shortcut.

## The governance boundary is about claims, not syntax

The same interface surface can be either honest or misleading depending on the claim that
surrounds it.

Honest claim:

- "objects passing this protocol check have a `close()` method we can call"

Misleading claim:

- "objects passing this protocol check are valid resources with correct cleanup semantics"

The difference is not technical cleverness. It is whether the language overstates what the
mechanism actually proves.

## When to pick each tool

Use an ABC when:

- the interface is part of the runtime design
- incomplete subclasses should fail clearly
- nominal ownership through inheritance is acceptable

Use a protocol when:

- structural compatibility matters more than inheritance
- the strongest value comes from static analysis
- you want flexible caller-side typing without base-class coupling

Use `__subclasshook__` when:

- an ABC needs a tiny structural concession
- the logic is trivial enough to stay reviewable
- you are willing to return `NotImplemented` instead of forcing cleverness

## What these tools do not replace

None of them replaces:

- behavioral tests
- performance evidence
- documentation of side effects
- review judgment about ownership and abstraction cost

That matters in Module 10 because interface syntax can make a design look more disciplined
than it really is.

## Review rules for interface contracts

When reviewing ABCs, protocols, or virtual subclass hooks, ask these questions:

- is the interface stable enough to deserve a name?
- does this design need runtime enforcement, static structural typing, or both?
- is the protocol check being asked to prove more than it can?
- does `__subclasshook__` stay trivial and default to `NotImplemented`?
- are semantic guarantees tested somewhere other than the interface declaration itself?

If the answer to the last question is "not really," the interface surface is doing too much
reputational work.

## What this page makes clear

The point is not "choose the fanciest contract surface."

The boundary is:

- nominal and structural contracts solve different problems
- runtime checks are often weaker than their names suggest
- governance begins when we stop overstating what an interface declaration proves

That is the habit that carries into the rest of the module.

## What to practice from this page

Try these before moving on:

1. Write one example where an ABC is clearer than a protocol.
2. Write one example where a protocol is better because inheritance would be artificial.
3. Reject one `__subclasshook__` idea that tries to smuggle business semantics into a structural check.

If those feel ordinary, the next step is to ask what happens after the interface exists:
how to preserve observability, reversibility, and test control when runtime behavior
becomes magical.

## Continue through Module 10

- Previous: [Dynamic Execution, Trust Boundaries, and Process Isolation](dynamic-execution-trust-boundaries-and-process-isolation.md)
- Next: [Observability, Reversibility, and Monkey-Patching Boundaries](observability-reversibility-and-monkey-patching-boundaries.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
