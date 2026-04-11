# Worked Example: Building a Minimal `@frozen` Class Decorator

The five core lessons in Module 06 become easier to trust when they meet one class tool
that is useful, tempting, and easy to overclaim.

A minimal `@frozen` decorator is exactly that kind of tool.

It combines:

- post-construction class transformation
- attribute-boundary control
- explicit limits around mutability
- a design decision about how much policy should live in one decorator

That makes it the right worked example for this module.

## The incident

Assume a team wants a small `@frozen` decorator for configuration-style classes.

They want it to:

- allow attributes to be assigned during initialization
- reject later reassignment and deletion
- stay readable to teammates who inspect the class
- avoid reaching for metaclasses

Those are reasonable goals. The mistake would be pretending this now creates deep or
universal immutability.

## The first design rule: define frozen at the surface

This example uses "frozen" in a deliberately narrow sense:

- instance attributes cannot be reassigned after initialization
- instance attributes cannot be deleted after initialization

This example does not claim:

- deep immutability of nested containers
- protection against every low-level escape hatch
- compile-time enforcement

That boundary keeps the example honest and teachable.

## Step 1: choose a post-construction design

Because the class already exists before the decorator runs, the decorator can install a
small amount of behavior after class creation.

That makes a class decorator a good fit when the rule is:

- opt-in
- uniform across the whole class
- visible in one place

This is exactly the boundary Module 06 is trying to teach.

## Step 2: allow initialization, then flip the boundary

The decorator needs one moment of flexibility during `__init__`, followed by a stricter
steady state afterward.

One simple design is:

1. wrap `__init__`
2. mark the instance as still initializing before running the original initializer
3. mark initialization as complete afterward
4. reject `__setattr__` and `__delattr__` once the object is settled

That keeps the state transition explicit instead of magical.

## Step 3: keep the interception rules narrow

The `__setattr__` override should reject only the post-initialization mutation boundary.

It should not:

- invent deep copy behavior
- try to freeze class attributes
- claim to secure every internal object graph

If the design needs those guarantees, this decorator is no longer the right owner.

## A bounded implementation

```python
import functools


def frozen(cls):
    original_init = getattr(cls, "__init__", object.__init__)
    original_setattr = getattr(cls, "__setattr__", object.__setattr__)
    original_delattr = getattr(cls, "__delattr__", object.__delattr__)

    @functools.wraps(original_init)
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, "_frozen_ready", False)
        try:
            original_init(self, *args, **kwargs)
        finally:
            object.__setattr__(self, "_frozen_ready", True)

    def __setattr__(self, name, value):
        if getattr(self, "_frozen_ready", False):
            raise AttributeError(
                f"{type(self).__name__} instances are frozen after initialization"
            )
        original_setattr(self, name, value)

    def __delattr__(self, name):
        if getattr(self, "_frozen_ready", False):
            raise AttributeError(
                f"{type(self).__name__} instances are frozen after initialization"
            )
        original_delattr(self, name)

    cls.__init__ = __init__
    cls.__setattr__ = __setattr__
    cls.__delattr__ = __delattr__
    return cls
```

## Why this version shows the right boundary

This decorator is useful because it keeps every important choice visible:

- the class is transformed after creation
- initialization still happens through the original constructor
- the mutation boundary is enforced through normal attribute hooks
- the policy is small enough to review in one pass

That is the kind of post-construction customization Module 06 is aiming for.

## Where the boundary shows up immediately

This decorator is intentionally surface-level.

For example:

```python
@frozen
class Settings:
    def __init__(self, tags):
        self.tags = tags


settings = Settings(["core", "api"])
settings.tags.append("admin")  # still allowed
```

The list object inside `tags` is still mutable. The decorator blocks rebinding
`settings.tags`, but it does not freeze the list itself.

That is not a bug in the example. That is the exact boundary.

## Why this does not need a metaclass

Nothing here depends on class-creation-time namespace control.

The decorator works because the needed policy can still be installed after the class
already exists:

- wrap the initializer
- override attribute mutation hooks
- return the modified class

That is strong evidence that a metaclass would be unnecessary escalation for this case.

## Questions to ask during review

When you see a frozen-class pattern like this, review it with these questions:

- does the decorator define frozen narrowly enough to stay truthful?
- is initialization still allowed explicitly before the object becomes frozen?
- are reassignment and deletion both covered?
- is the design pretending to guarantee deep immutability when it only controls the instance surface?
- would a plain explicit class be clearer if only one class needs this behavior?

## What this example makes clear about Module 06

This worked example ties the module together:

- class decorators can install post-construction behavior
- dataclass-style convenience is different from immutability policy
- attribute control lives at the `__setattr__` and `__delattr__` boundary
- the smallest honest owner matters more than using the most powerful tool

That is the durable takeaway. The decorator is here as a clean case study in class
customization boundaries, not as a universal immutability recipe.

## Continue through Module 06

- Previous: [Class Customization Boundaries](class-customization-boundaries.md)
- Next: [Exercises](exercises.md)
- Reference: [Exercise Answers](exercise-answers.md)
- Terms: [Glossary](glossary.md)
