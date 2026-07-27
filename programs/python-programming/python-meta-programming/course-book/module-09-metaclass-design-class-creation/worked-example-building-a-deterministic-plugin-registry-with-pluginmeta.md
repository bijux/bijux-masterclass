# Worked Example: Building a Deterministic Plugin Registry with `PluginMeta`


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Metaclass Design Class Creation"]
  page["Worked Example: Building a Deterministic Plugin Registry with `PluginMeta`"]
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

The five core lessons in Module 09 become much easier to trust when they meet one
metaclass design that is useful, tempting, and still narrow enough to review honestly.

Deterministic plugin registration is exactly that kind of case.

It combines:

- class-creation-time registration
- hierarchy-wide automatic behavior
- duplicate rejection
- resettable global state for tests

That makes it the right worked example for the module.

This page should be read as a review packet, not as a recipe to copy into every plugin
system. The teaching goal is to show one bounded case where the metaclass still has an
honest owner.

## The incident

Assume a team wants a plugin family where:

- concrete subclasses register automatically
- base classes can opt out as abstract
- plugin names are unique within a group
- tests can reset the registry deterministically

Those are reasonable goals. The mistake would be pretending that every registry problem now
deserves a metaclass.

## Evidence route for reading this example honestly

Work through the example in this order:

| Review step | What to inspect | What strong evidence looks like |
| --- | --- | --- |
| Name the invariant | What must always happen when concrete subclasses are defined? | Registration, duplicate rejection, and deterministic grouping are explicit |
| Name the rejected owner | Why not use a decorator or explicit registry call? | The answer explains what automatic subclass-time behavior would be lost |
| Audit import-time cost | What global state changes during import? | Registry mutation, ordering, and reset needs are stated plainly |
| Inspect reset discipline | How do tests recover determinism? | A clear reset surface exists and is part of the design |
| Reject overclaim | What is intentionally outside this example? | Discovery, lifecycle, and configuration are excluded explicitly |

## The first design rule: justify the metaclass narrowly

This example uses a metaclass because the desired behavior is:

- tied to class creation itself
- automatic across the subclass hierarchy
- not just a one-off post-creation transformation

That is the boundary the module has been building toward.

If the same system only needed occasional opt-in registration, a decorator or explicit
registry call might still be clearer.

Keep the refusal sentence close:

if the family can tolerate opt-in registration, the metaclass case becomes much weaker.

## Step 1: keep abstract opt-out explicit

The metaclass should not blindly register every class it sees.

A small convention such as:

```python
__abstract__ = True
```

lets base classes participate in the hierarchy without being treated as concrete plugin
implementations.

That keeps the registry focused on real entries.

## Step 2: derive the group deterministically

The example should make group selection visible and predictable.

A good small rule is:

- use `group` from the class body if present
- otherwise inherit the first available group from base classes
- otherwise fall back to a default group

This rule is simple enough to explain in review.

## Ownership table for the example

| Design concern | Owner in this example | Why that owner is honest |
| --- | --- | --- |
| Decide whether a class is abstract | Class body flag plus metaclass read | The class states intent; the metaclass applies the family rule |
| Derive the final group | Metaclass at class creation time | The class family needs one automatic place to settle grouping |
| Reject duplicate plugin names | Metaclass during registration | The family rule must hold for every concrete subclass |
| Provide reset for tests | Explicit classmethod support | Reset is operational support, not the invariant itself |

## Step 3: make duplicate rejection and ordering explicit

A registry is not honest unless it answers two questions:

- what happens on duplicate names?
- what order do tests and callers observe?

This example rejects duplicates within a group and sorts registrations deterministically by
name so test behavior stays predictable.

The review benefit is important:

- duplicate handling is named, not implied
- observed order is named, not left to import accidents
- reset is built in, not postponed to test folklore

## A bounded implementation

```python
from collections import defaultdict
from threading import RLock


_registry = defaultdict(list)
_lock = RLock()


class PluginMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)

        if namespace.get("__abstract__", False):
            return cls

        group = namespace.get("group")
        if group is None:
            for base in bases:
                if hasattr(base, "group"):
                    group = getattr(base, "group")
                    break
        if group is None:
            group = "default"
        cls.group = group

        with _lock:
            items = _registry[group]
            if any(existing_name == name for existing_name, _ in items):
                raise ValueError(f"duplicate plugin {name!r} in group {group!r}")
            items.append((name, cls))
            items.sort(key=lambda item: item[0])

        return cls

    @classmethod
    def get_plugins(mcs, group):
        with _lock:
            return list(_registry.get(group, []))

    @classmethod
    def clear(mcs, group=None):
        with _lock:
            if group is None:
                _registry.clear()
            else:
                _registry.pop(group, None)


class Logger(metaclass=PluginMeta):
    __abstract__ = True
    group = "logging"

    def log(self, message):
        raise NotImplementedError


class FileLogger(Logger):
    def log(self, message):
        return f"[FILE] {message}"


class ConsoleLogger(Logger):
    def log(self, message):
        return f"[CONSOLE] {message}"
```

## Why the code stays bounded

Notice what the metaclass is not doing:

- no package scanning
- no enable or disable policy
- no runtime lifecycle hooks
- no dependency graph management

That restraint is part of why the example remains teachable.

## Why this is useful for review

This example keeps the important metaclass choices visible:

- registration happens during class creation
- the effect is hierarchy-wide
- abstract opt-out is explicit
- duplicate handling is part of the rule
- tests get a reset hook through `clear()`

That makes it a real metaclass case study instead of a generic “look what metaclasses can
do” demo.

## Review notes another learner should be able to write

After reading the implementation, a strong learner should be able to say:

- "registration is the class-creation invariant"
- "the metaclass is justified because every concrete subclass must register automatically"
- "reset helpers are necessary because import-time state is mutated"
- "this still is not a full plugin framework"

## Why import-time effects still matter here

Even though this is a good metaclass example, it still has real costs:

- registration depends on class definition happening
- import order affects when plugins appear
- reload can register classes again unless tests or tooling reset state

Those are not flaws in the explanation. They are part of the design truth.

## Failure modes if this example grows without discipline

| Growth mistake | What breaks |
| --- | --- |
| Add discovery and loading into the metaclass | Import-time cost and hidden coupling increase sharply |
| Hide reset outside the registry API | Tests become harder to isolate honestly |
| Treat duplicate rejection as optional policy | The invariant stops being precise |
| Claim the example manages plugins end to end | The teaching boundary becomes false |

## Why this is narrower than a plugin framework

This example is only about:

- registration
- uniqueness
- deterministic ordering
- test reset

It does not attempt:

- plugin discovery across packages
- enable or disable policies
- configuration injection
- lifecycle management

Those would push the design beyond a single metaclass example into broader framework
architecture.

## What this example makes clear about Module 09

This worked example ties the module together:

- metaclass behavior happens at class creation time
- hierarchy-wide behavior can justify the tool
- global state needs explicit reset paths
- import-time consequences must be named, not hidden
- the metaclass remains justified only because the ownership boundary is narrow and clear

That is the durable takeaway. The point is not to make registries feel magical. The point
is to show one case where class-creation-time control is genuinely the honest owner.

## Exit check for this page

Before moving on, make sure you can do all of the following:

- name the exact class-creation invariant the metaclass owns
- explain why explicit opt-in registration would change the design meaningfully
- identify one import-time cost and one reset response
- state two plugin-system concerns this example intentionally does not own

## Continue through Module 09

- Previous: [Metaclass Boundaries and Class-Creation Ownership](metaclass-boundaries-and-class-creation-ownership.md)
- Next: [Exercises](exercises.md)
- Reference: [Exercise Answers](exercise-answers.md)
- Terms: [Glossary](glossary.md)
