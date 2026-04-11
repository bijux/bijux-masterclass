# Design Boundaries

<!-- page-maps:start -->
## Guide Maps

```mermaid
graph TD
  boundary["Design boundaries"] --> wrapper["Callable boundary"]
  boundary --> attribute["Attribute boundary"]
  boundary --> class_creation["Class-creation boundary"]
  boundary --> governance["Governance boundary"]
```

```mermaid
flowchart LR
  question["Name the behavior you want to add or review"] --> owner["Choose the owning boundary"]
  owner --> lower["Check the lower-power alternative first"]
  lower --> evidence["Inspect the matching command, file, or test"]
  evidence --> decision["Leave with a keep, change, or reject call"]
```
<!-- page-maps:end -->

Use this guide when the capstone technically makes sense but you still need to know why
each mechanism owns the behavior it owns. The goal is to keep the capstone small, honest,
and reviewable instead of letting it drift into "the framework can do anything."

## Callable boundary

**Owner:** `actions.py`

This boundary owns:

- action wrapping
- preserved signatures and metadata
- action-history recording

This boundary does not own:

- field validation
- class registration
- manifest assembly

Reject or redesign when:

- the wrapper starts reaching into per-instance storage
- retry, caching, or validation policy swallows the original callable contract
- reviewers can no longer tell what the wrapped action really accepts

## Attribute boundary

**Owner:** `fields.py`

This boundary owns:

- descriptor-backed configuration rules
- coercion and validation for one field
- field metadata exported through the manifest

This boundary does not own:

- plugin registration
- action invocation behavior
- broad orchestration policy

Reject or redesign when:

- a descriptor starts owning behavior that is not really about attribute access
- per-instance state leaks across instances
- field objects begin to look like a hidden framework layer

## Class-creation boundary

**Owner:** `framework.py`

This boundary owns:

- plugin registration
- generated constructor signatures
- manifest assembly from declared fields and actions

This boundary does not own:

- concrete delivery behavior
- descriptor coercion details
- invocation history recording

Reject or redesign when:

- the metaclass exists only because it feels powerful
- a class decorator or explicit registration step could own the same rule more honestly
- class-definition work becomes surprising, heavy, or untestable

## Governance boundary

**Owners:** `cli.py`, tests, and the proof guides

This boundary owns:

- public inspection and invocation routes
- saved review bundles
- executable confirmation through tests

This boundary does not own:

- private magic that cannot be reached from the public surface
- unreviewable import-time tricks
- dynamic execution hidden from ordinary inspection routes

Reject or redesign when:

- the runtime becomes easier to use than to observe
- debugging now requires folklore instead of public commands and tests
- the proof route no longer matches the design claims the capstone is meant to defend

## Definition-time sequence

1. `PluginMeta.__prepare__` returns `DefinitionNamespace`.
2. The class body executes and places fields and wrapped actions into that namespace.
3. Descriptors receive `__set_name__` and learn their storage keys.
4. `PluginMeta.__new__` gathers inherited and local fields and action specs.
5. A constructor signature is generated from the collected fields.
6. Concrete plugins receive their group and public plugin name.
7. Concrete plugins are registered in the deterministic runtime registry.

## Choose the lowest-power honest mechanism

| If the requirement is about... | Prefer this mechanism | First owning surface |
| --- | --- | --- |
| configuration validation, defaults, or schema metadata | descriptor | `fields.py` |
| invocation metadata, preserved signatures, or action history | decorator | `actions.py` |
| class registration, generated constructors, or manifest assembly | metaclass or framework helper | `framework.py` |
| one concrete adapter behavior | ordinary plugin class | `plugins.py` |
| one public inspection or invocation route | CLI command | `cli.py` |

## Strong proof pairings

- pair descriptors with `make field` and `tests/test_fields.py`
- pair decorators with `make action`, `make trace`, and runtime tests
- pair metaclass changes with `make registry`, `make signatures`, and `tests/test_registry.py`
- pair plugin changes with `make plugin`, `make demo`, and runtime tests
- pair CLI changes with `tests/test_cli.py` and the closest saved bundle route

## Best companion guides

- `ARCHITECTURE.md`
- `PACKAGE_GUIDE.md`
- `EXTENSION_GUIDE.md`
- `TEST_GUIDE.md`
