# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
collect more class tricks. The goal is to make class-level ownership, attribute
boundaries, and escalation decisions explicit.

Each exercise asks for three things:

- the class rule or invariant you are trying to enforce
- the class-level tool you chose
- the reason that choice is the smallest honest owner

## Exercise 1: Use one class decorator for an opt-in class rule

Write or inspect a class decorator that adds one visible post-construction behavior.

What to hand in:

- the behavior it adds
- one sentence explaining why the class decorator can install it after class creation
- one sentence explaining why this does not need a metaclass

## Exercise 2: Separate dataclass generation from validation

Create or review a small `@dataclass` example with defaults and generated methods.

What to hand in:

- the generated behavior you are relying on
- one invariant that the dataclass still does not enforce for you
- one sentence describing where that missing rule should live instead

## Exercise 3: Control one attribute boundary with a property

Implement one property that protects a single attribute.

What to hand in:

- the attribute rule it enforces
- one setter or getter behavior that makes the boundary visible
- one explanation of why a property is clearer here than a class-wide hook

## Exercise 4: Promote one repeated property rule into a descriptor

Take a repeated field rule and sketch or build a reusable descriptor for it.

What to hand in:

- the repeated rule
- one reason the rule is now better owned by a descriptor than by copied properties
- one sentence explaining why this is still different from metaclass control

## Exercise 5: Place one design on the lower-power ladder

Choose one class customization requirement and place it on this ladder:

- plain class code
- class decorator
- property
- descriptor
- metaclass

What to hand in:

- the requirement
- the level you chose
- one sentence rejecting at least one stronger option as unnecessary

## Exercise 6: Review the limits of a frozen surface

Use the worked example pattern on a minimal `@frozen` decorator or a similar design.

What to hand in:

- the exact mutation boundary the decorator controls
- one kind of mutation it still allows
- one explanation of why that remaining mutability does not make the example dishonest

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you distinguish generated convenience from real policy ownership
- you keep attribute control at the narrowest honest boundary
- you treat descriptors as reusable attribute tools, not as prestige mechanisms
- you reject metaclass escalation when post-construction or attribute-boundary tools are still enough

If an answer still sounds like "the class magic handles it," keep going.
