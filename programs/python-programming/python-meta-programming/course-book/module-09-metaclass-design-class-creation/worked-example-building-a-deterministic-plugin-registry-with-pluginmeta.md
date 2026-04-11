# Worked Example: Building a Deterministic Plugin Registry with `PluginMeta`

The five core lessons in Module 09 become much easier to trust when they meet one
metaclass design that is useful, tempting, and still narrow enough to review honestly.

Deterministic plugin registration is exactly that kind of case.

It combines:

- class-creation-time registration
- hierarchy-wide automatic behavior
- duplicate rejection
- resettable global state for tests

That makes it the right worked example for the module.

## The incident

Assume a team wants a plugin family where:

- concrete subclasses register automatically
- base classes can opt out as abstract
- plugin names are unique within a group
- tests can reset the registry deterministically

Those are reasonable goals. The mistake would be pretending that every registry problem now
deserves a metaclass.

## The first design rule: justify the metaclass narrowly

This example uses a metaclass because the desired behavior is:

- tied to class creation itself
- automatic across the subclass hierarchy
- not just a one-off post-creation transformation

That is the boundary the module has been building toward.

If the same system only needed occasional opt-in registration, a decorator or explicit
registry call might still be clearer.

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

## Step 3: make duplicate rejection and ordering explicit

A registry is not honest unless it answers two questions:

- what happens on duplicate names?
- what order do tests and callers observe?

This example rejects duplicates within a group and sorts registrations deterministically by
name so test behavior stays predictable.

## A didactic implementation

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

## Why this is a good teaching artifact

This example keeps the important metaclass choices visible:

- registration happens during class creation
- the effect is hierarchy-wide
- abstract opt-out is explicit
- duplicate handling is part of the rule
- tests get a reset hook through `clear()`

That makes it a real metaclass case study instead of a generic “look what metaclasses can
do” demo.

## Why import-time effects still matter here

Even though this is a good metaclass example, it still has real costs:

- registration depends on class definition happening
- import order affects when plugins appear
- reload can register classes again unless tests or tooling reset state

Those are not flaws in the explanation. They are part of the design truth.

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

## What this example teaches about Module 09

This worked example ties the module together:

- metaclass behavior happens at class creation time
- hierarchy-wide behavior can justify the tool
- global state needs explicit reset paths
- import-time consequences must be named, not hidden
- the metaclass remains justified only because the ownership boundary is narrow and clear

That is the real lesson. The point is not to make registries feel magical. The point is to
show one case where class-creation-time control is genuinely the honest owner.
