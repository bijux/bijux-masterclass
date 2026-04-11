# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
make metaclasses feel more advanced. The goal is to make class-creation ownership,
definition-time timing, and lower-power alternatives explicit.

Each exercise asks for three things:

- the class-creation or hierarchy rule you are trying to enforce
- the metaclass or lower-power owner you chose
- the reason that choice is the clearest one

## Exercise 1: Build one class manually with `type(...)`

Create one tiny class dynamically with `type(name, bases, namespace)`.

What to hand in:

- what each of the three arguments contributes
- one piece of metadata you set manually
- one explanation of why this is still lower-power than a custom metaclass

## Exercise 2: Trigger and explain one metaclass conflict

Construct a small multiple-inheritance example that raises a metaclass conflict.

What to hand in:

- the conflicting bases or metaclasses
- the error you get
- one explanation of why this is an ownership conflict instead of just a syntax problem

## Exercise 3: Split one metaclass across `__new__` and `__init__`

Build or inspect one metaclass that does structural work and one bookkeeping task.

What to hand in:

- the rule that belongs in `__new__`
- the bookkeeping that belongs in `__init__`
- one sentence explaining why swapping them would make the design worse

## Exercise 4: Use `__prepare__` for one declaration-time rule

Create or inspect one custom namespace mapping supplied by `__prepare__`.

What to hand in:

- the declaration-time fact it captures or enforces
- why later hooks would miss or reconstruct that fact poorly
- one explanation of why the custom mapping is still narrow enough to review

## Exercise 5: Reject one unnecessary metaclass

Take one metaclass proposal and rewrite it mentally as a lower-power design.

What to hand in:

- the original metaclass idea
- the lower-power replacement
- one sentence explaining what the metaclass was not actually needed for

## Exercise 6: Review the plugin registry example honestly

Use the worked example as a case study.

What to hand in:

- one thing the metaclass owns honestly
- one import-time or testing risk it still introduces
- one explanation of why this is narrower than a general plugin framework

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you explain metaclass behavior in class-creation language
- you keep import-time effects visible
- you separate structural hooks from bookkeeping hooks
- you use `__prepare__` only when declaration-time facts really matter
- you reject metaclass escalation when lower-power tools remain honest owners

If an answer still sounds like "a metaclass can just handle it," keep going.
