# Exercise Answers


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Class Customization Pre Metaclasses"]
  page["Exercise Answers"]
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

## Answer 7: Separate repeated field policy from class-wide policy

Example answer:

Suppose several classes each need normalized email fields and trimmed name fields.

Strong assessment:

- `__post_init__` can work when the rule is local to one dataclass instance boundary
- a property is good when one field in one class needs a visible read/write boundary
- a descriptor is stronger when the same attribute rule repeats across several classes or fields

Good conclusion:

The owner should follow the repetition pattern. Repeated field policy belongs at the
attribute boundary, not in copied class-local code or a broader class-wide mechanism.

## Answer 8: Reject one unnecessary escalation to metaclass power

Example answer:

Requirement:

- register classes after definition and enforce one naming convention

Better owner:

- a class decorator plus ordinary validation logic

Strong explanation:

- the requirement does not need custom namespace preparation
- it does not need to change class creation protocol itself
- the class already exists before the rule needs to run

Good conclusion:

A real metaclass need is still missing because nothing here depends on controlling how the
class object is built. Post-construction customization is enough.

## Answer 9: Compare honest class claims with overstated class claims

Example answer:

Honest description:

- "This decorator prevents reassignment of top-level instance attributes after initialization."

Overstated description:

- "This makes instances fully immutable."

Good conclusion:

The second version is misleading because words such as "fully" and "immutable" imply deep
and universal guarantees the tool does not actually provide. Honest language keeps the
attribute-surface boundary visible.

## Answer 10: Produce a class-boundary packet

The packet is strong when another learner can answer:

- which invariant is being enforced
- which owner carries it directly
- which stronger mechanism was rejected and why
- where generated convenience ends and real policy ownership begins

## What strong Module 06 answers have in common

Across the whole set, strong answers share the same habits:

- they separate generated convenience from real invariants
- they keep rules at the smallest honest boundary
- they treat descriptors as reusable attribute owners, not as a shortcut to extra prestige
- they reject metaclass escalation unless class-creation-time control is truly required
- they distinguish repeated field policy from real class-creation policy
- they leave behind a packet another learner can review without guessing

If an answer still sounds like "a more advanced class feature could handle it," revise it
until you can say why the chosen owner is the clearest one.

## Continue through Module 06

- Previous: [Exercises](exercises.md)
- Return: [Overview](index.md)
- Next module: [Module 07](../module-07-descriptors-lookup-attribute-control/index.md)
- Terms: [Glossary](glossary.md)
