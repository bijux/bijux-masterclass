# Hint-Driven Validation and Coercion

The fourth pressure in Module 08 is metadata.

Once a descriptor starts reading annotations and `Annotated[...]` metadata, it stops being
only a storage hook and starts acting like a lightweight model system.

That can be useful. It can also become misleading very quickly.

## The sentence to keep

Hint-driven descriptors use type annotations as runtime evidence for limited validation and
coercion, but they stay honest only when the supported hint surface and coercion rules are
named explicitly.

That is the difference between a useful field system and fake comprehensiveness.

## What this pattern is trying to do

Hint-aware field descriptors usually want to do some mix of these:

- read a declared type from `get_type_hints`
- use that type for `isinstance`-style checks
- apply metadata validators from `Annotated[...]`
- coerce a narrow set of values into supported scalar types

That can create a very expressive declarative field surface.

It also raises the risk of overclaiming what “runtime typing support” really means.

## A narrow runtime checker

```python
from typing import Any, Union, get_args, get_origin
import types


def supports_instance(value, hint):
    if hint is Any:
        return True

    origin = get_origin(hint)
    if origin in (Union, types.UnionType):
        return any(supports_instance(value, arg) for arg in get_args(hint))

    if origin is not None:
        raise NotImplementedError(
            "parameterized generics are intentionally unsupported here"
        )

    return isinstance(value, hint)
```

This is the right educational shape because it says clearly what it does not support.

## A hint-aware field

```python
from typing import Annotated, Any, get_args, get_origin, get_type_hints


class HintField:
    def __set_name__(self, owner, name):
        hints = get_type_hints(owner)
        self.public_name = name
        self.private_name = f"_{name}"
        self.hint = hints[name]

        origin = get_origin(self.hint)
        if origin is Annotated:
            base, *metadata = get_args(self.hint)
            self.hint = base
            self.validators = [item for item in metadata if callable(item)]
        else:
            self.validators = []

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.private_name)

    def __set__(self, obj, value):
        if not supports_instance(value, self.hint):
            for candidate in (int, float, str):
                if candidate is self.hint:
                    try:
                        value = candidate(value)
                        break
                    except Exception:
                        pass
            else:
                raise TypeError(f"{self.public_name} cannot coerce {value!r} to {self.hint!r}")

        if not supports_instance(value, self.hint):
            raise TypeError(f"{self.public_name} expected {self.hint!r}")

        for validator in self.validators:
            value = validator(value)

        obj.__dict__[self.private_name] = value
```

This is useful because it keeps the whole pipeline visible:

- resolve hints once
- extract metadata validators
- coerce conservatively
- validate after coercion
- store the accepted value

## Why `Annotated[...]` is a good fit here

`Annotated[...]` works well for field systems because it lets the type and the extra
runtime metadata travel together.

For example:

```python
Annotated[str, min_length(3)]
```

can mean:

- the base type is `str`
- the metadata carries extra validators

That creates a clean declarative surface as long as the runtime system stays narrow about
what metadata it understands.

## Coercion is where honesty matters most

Coercion can make field systems pleasant to use, but it also creates ambiguity.

That is why this module treats coercion conservatively:

- support a very small scalar subset
- fail loudly when conversion is unclear
- do not pretend to support all typing constructs

If the descriptor silently guesses too much, it becomes harder to trust.

## Unsupported surfaces should be refused clearly

Strong hint-driven designs are explicit about what they do not handle.

Examples often refused at this stage include:

- parameterized generics such as `list[int]`
- nested model validation
- arbitrary custom typing constructs

Refusing those surfaces is a design strength, not a weakness.

## Why this is framework-adjacent

Once a field descriptor reads type hints, applies metadata validators, and coerces values,
it starts to resemble lightweight versions of tools such as Pydantic or attrs.

That resemblance is useful for learning, but it creates a new boundary question:

is this still a field-level convenience, or is it drifting into a broader model framework?

The next core will answer that directly.

## Review rules for hint-driven fields

When reviewing hint-aware descriptors, keep these questions close:

- which hint forms are actually supported?
- what coercions are allowed, and are they conservative enough?
- what metadata from `Annotated[...]` is recognized?
- are unsupported hint surfaces refused clearly?
- is this still a field descriptor, or is it quietly trying to become a model framework?

## What to practice from this page

Try these before moving on:

1. Implement one hint-aware field that supports plain classes plus `Union` or `Optional`.
2. Add one `Annotated[...]` validator and explain when it runs relative to coercion.
3. Write one short review note rejecting a claim of “full runtime typing support.”

If those feel ordinary, the next step is the module's design page: where descriptor
systems stop being just fields and start needing broader framework ownership.
