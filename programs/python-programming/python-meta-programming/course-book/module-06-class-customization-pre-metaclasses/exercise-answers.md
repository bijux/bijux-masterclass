# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that keep
class-level power, attribute boundaries, and escalation limits honest.

## Answer 1: Use one class decorator for an opt-in class rule

Example answer:

A class decorator that registers decorated classes in a plugin registry is a good fit
when:

- registration is opt-in
- the class already exists before registration runs
- the effect can be inspected after decoration

Good conclusion:

This does not need a metaclass because the rule does not depend on controlling namespace
preparation or class creation itself. The decorator can apply the behavior after the class
object already exists.

## Answer 2: Separate dataclass generation from validation

Example answer:

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int = 0
```

Generated behavior:

- `__init__`
- `__repr__`
- equality methods

Missing invariant:

- `age` is not automatically checked to be non-negative

Good conclusion:

The missing rule should live in an explicit validation boundary such as `__post_init__`, a
property, or a descriptor, depending on how broad the rule becomes.

## Answer 3: Control one attribute boundary with a property

Example answer:

```python
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be non-negative")
        self._price = value
```

Good conclusion:

A property is the clearest owner because the rule applies to one field and stays visible
exactly where reads and writes cross the attribute boundary.

## Answer 4: Promote one repeated property rule into a descriptor

Example answer:

Suppose several classes each need string attributes that must be non-empty.

A descriptor is now a better fit because:

- the same rule repeats across multiple attributes or classes
- one reusable owner is clearer than copied property setters
- the rule still lives at the attribute boundary

Good conclusion:

This is still not metaclass control because the descriptor governs how specific
attributes behave on access and assignment, not how the class itself is created.

## Answer 5: Place one design on the lower-power ladder

Example answer:

Requirement:

- keep one `email` field normalized to lowercase on assignment

Best placement:

- property

Rejected stronger options:

- a descriptor is unnecessary if only one attribute in one class needs the rule
- a metaclass would be extreme overreach because no class-creation control is required

Good conclusion:

Strong answers do not just pick a tool. They explain why a stronger tool would add power
without adding clarity.

## Answer 6: Review the limits of a frozen surface

Example answer:

A minimal `@frozen` decorator can honestly control:

- reassignment of instance attributes after initialization
- deletion of instance attributes after initialization

It still allows:

- mutation of nested mutable objects such as lists or dictionaries already stored on the instance

Good conclusion:

That remaining mutability does not make the example dishonest as long as the decorator
defines frozen as a surface-level attribute rule rather than as universal deep
immutability.

## What strong Module 06 answers have in common

Across the whole set, strong answers share the same habits:

- they separate generated convenience from real invariants
- they keep rules at the smallest honest boundary
- they treat descriptors as reusable attribute owners, not as a shortcut to extra prestige
- they reject metaclass escalation unless class-creation-time control is truly required

If an answer still sounds like "a more advanced class feature could handle it," revise it
until you can say why the chosen owner is the clearest one.
