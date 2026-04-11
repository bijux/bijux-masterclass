# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that keep
class-creation power, import-time behavior, and lower-power alternatives honest.

## Answer 1: Build one class manually with `type(...)`

Example answer:

- `name` becomes the class name
- `bases` determines inheritance
- `namespace` supplies methods and attributes

Useful metadata:

- `__module__` can be set manually so the class has a sensible module identity

Good conclusion:

This is still lower-power than a metaclass because it creates one class explicitly without
automatically changing how future subclasses are created.

## Answer 2: Trigger and explain one metaclass conflict

Example answer:

If `A` uses `MetaA` and `B` uses `MetaB`, then:

```python
class Bad(A, B):
    pass
```

may raise a metaclass conflict because Python cannot find one compatible class-creation
owner for the new class.

Good conclusion:

The error is not just syntax friction. It is a signal that two incompatible class-creation
authorities are being combined without a coherent shared owner.

## Answer 3: Split one metaclass across `__new__` and `__init__`

Example answer:

- `__new__` should enforce a required method or inject a structural attribute before the class is finalized
- `__init__` should append the finished class to a registry

Good conclusion:

Swapping them makes the design blur structure and bookkeeping. `__new__` owns class-shape
decisions; `__init__` owns post-creation bookkeeping.

## Answer 4: Use `__prepare__` for one declaration-time rule

Example answer:

A custom mapping can reject duplicate non-dunder assignments during class body execution.

Why later hooks are worse:

- after the class body finishes, only the final value may remain unless the mapping
  recorded the duplicate event during assignment

Good conclusion:

`__prepare__` is justified only when the class-body-time fact truly matters and cannot be
recovered cleanly later.

## Answer 5: Reject one unnecessary metaclass

Example answer:

Original idea:

- use a metaclass to register classes in a plugin list

Lower-power replacement:

- use an explicit decorator or helper function for opt-in registration

Good conclusion:

If post-creation registration is enough, the metaclass was not actually needed. The design
does not require class-creation control just because automatic registration sounds neat.

## Answer 6: Review the plugin registry example honestly

Example answer:

Honest metaclass ownership:

- automatically registering every concrete subclass at class-creation time

Remaining risk:

- import order and reload behavior still affect when entries appear and whether tests need reset hooks

Why it is narrower than a full framework:

- it handles registration and ordering only, not discovery, lifecycle management, or configuration

Good conclusion:

The example is justified because the metaclass owns one clear hierarchy-wide class-creation
rule, not because registries are automatically “metaclass territory.”

## What strong Module 09 answers have in common

Across the whole set, strong answers share the same habits:

- they explain metaclasses in class-creation language
- they keep import-time effects visible
- they separate `__new__`, `__init__`, and `__prepare__` by responsibility
- they treat conflicts as design signals
- they reject metaclass escalation when lower-power tools still own the problem honestly

If an answer still sounds like "metaclasses are powerful so they fit here," revise it
until you can name the exact class-creation invariant they own and why lower-power tools
fail.
