# Copying and Cloning – Shallow, Deep, and Custom Semantics

## Introduction

This core investigates the semantics of object copying in Python, contrasting shallow and deep copies from the `copy` module with custom implementations via `__copy__` and `__deepcopy__`. Extending aliasing hazards from M01C06 and the value/entity distinction from M01C01, we delineate copy strategies for entities (identity-preserving), value objects (interchangeable duplicates), and aggregates (nested structures), while identifying when copying signals deeper design flaws. Appropriate copying neutralizes sharing risks without unnecessary overhead, ensuring semantic fidelity across duplicates.

The layered structure persists: language-level semantics outline guarantees, CPython notes detail optimizations, design semantics guide modeling choices, and practical guidelines furnish prescriptive rules. This framework yields a portable model for replication, resilient across implementations.

Cross-references link to prerequisites: shared state perils in M01C06; dataclass copying pitfalls in M03C24. Proficiency here enables judicious duplication, distinguishing solutions from symptoms of over-sharing.

## 1. Copy Protocols on Top of the Data Model

Python's `copy` module provides shallow and deep copying *protocols* on top of the core data model, with optional dunder overrides for customization. This is library-level behaviour, not part of the core language spec, but in practice it forms part of Python’s “design surface”. Copying addresses aliasing by creating new container/instance objects, but it does not change the fact that identity is per-object and references can still be shared.

### Shallow and Deep Copy Protocols

**Typical behaviour (CPython and similar)**:
- `copy.copy(obj)` creates a *shallow* copy: a new container/instance whose fields/elements reference the **same underlying objects** as the original. There is no recursive copying.
- `copy.deepcopy(obj)` recursively deep-copies: a new object graph where nested mutable objects are also copied (subject to the type-specific rules and the memo). Sharing between the original and the copy is broken, but aliasing *inside* the original graph is normally preserved inside the copy via the `memo` table (if two attributes pointed at the same list before, they point at the same new list after).
- For many atomic or “effectively atomic” types (e.g. functions, modules, some resource handles), both operations simply return the original object. For types that truly have no meaningful copy semantics, the correct behaviour is to raise (typically `TypeError`) rather than fake a copy.
- Custom hooks: `__copy__(self)` overrides shallow semantics; `__deepcopy__(self, memo)` overrides deep copy. `memo` is a dict used to detect and handle cycles and to preserve or re-establish sharing where desired; it is keyed by `id(obj)`.

Example (portable, contrasting behaviors):

```python
import copy

class Container:
    def __init__(self):
        self.primitives = [1, 2]
        self.nested = [[3], [4]]

orig = Container()
shallow = copy.copy(orig)
deep = copy.deepcopy(orig)

shallow.primitives.append(5)  # orig.primitives also [1, 2, 5]
shallow.nested[0].append(6)   # orig.nested also affected

deep.primitives.append(7)     # orig unaffected
deep.nested[0].append(8)      # orig unaffected
```

In the default implementations, copies preserve the concrete type and the externally-visible state, but not identity. Custom hooks are free to diverge from this (e.g. reset internal caches, change IDs, or even return the original object for immutables).

### Custom Copy Semantics

**Contract for custom hooks**:
- `__copy__` should return an object that is a valid “shallow copy” according to the type’s own semantics. For immutable types, returning `self` is acceptable.
- `__deepcopy__` receives a `memo` dict for cycle detection; it should either return a new instance or, for immutables or “atomic” objects, an appropriate shared instance (often `self`).
- Neither hook is invoked automatically by the interpreter; they are only used when you call into the `copy` module.

These protocols enable semantic cloning without mandating deep traversal for all cases.

## 2. Implementation Notes (CPython, non-normative)

CPython's `copy` module uses type-dependent dispatch and, for deep copy, recursive traversal with memoization.

- **Shallow Copy**: `_copy_dispatch` first looks for a `__copy__` method. Otherwise, it uses type-specific strategies (e.g. `list()` for lists, `dict.copy()` for dicts, `type(obj).__new__` plus `__dict__`/slot copying for plain instances). For many atomic builtins it just returns the original object.
- **Deep Copy**: `_deepcopy_dispatch` recurses on attributes/elements, using `id(obj)` as keys in `memo` to break cycles and optionally preserve sharing. Builtins have specialized fast paths (e.g. list/tuple comprehensions).
- **Performance Nuances**: Shallow copy is typically O(n) in the number of top-level fields/elements; deep copy scales with the size of the reachable object graph and can hit recursion limits (`sys.getrecursionlimit()`) on deep structures. Memoization prevents exponential blow-up on DAGs.
- **Edge Cases**: Objects that participate in pickling via `__reduce__`/`__getstate__` often integrate cleanly with `copy`. Truly unsupported objects may raise `TypeError` when deep-copied. Resource-owning objects (files, sockets, DB sessions) typically cannot be meaningfully deep-copied and should either opt out or define a very constrained snapshot semantics.

These optimize common graphs but expose no privacy—copies probe state directly.

## 3. Design Semantics

Copying aligns with the value/entity lens (M01C01): value-like objects often do not need copying at all if they are truly immutable; entity-like ones may need custom identity semantics; aggregates sometimes require deep copying to neutralise nested sharing (M01C06) and sometimes must *not* deep-copy because that would destroy intentional sharing or live resource handles.

- **Semantics by Type**:
  - *Pure values (immutable)*: copying is usually unnecessary; `copy.copy`/`copy.deepcopy` can safely return `self` in custom hooks.
  - *Composite values (contain mutables)*: if you want “new value, independent internals”, deep copy (or an explicit domain-level clone) is more appropriate than shallow.
  - *Entities*: `__copy__` may need to inject a new identity (e.g. new ID) while preserving some fields; often you explicitly *forbid* deep copies because they don’t make sense for identity-bearing objects.
  - *Aggregates*: deep copy is sometimes required to break sharing between aggregates; other times you want to preserve certain shared sub-objects or resource handles. Here `__deepcopy__` and `memo` must encode domain rules explicitly; naïve deep copy of an aggregate that wraps I/O or locks is often a bug.
- **When Copying is a Smell**: If you find yourself copying objects frequently just to avoid surprising mutations from other parts of the system, that usually signals over-sharing and poor ownership boundaries. Prefer immutability, clearer ownership, or explicit “snapshot”/“clone” operations over ad hoc copying.
- **Custom Hooks**: Override for domain logic (e.g., `__deepcopy__` cloning relations); ensure memo respects cycles.

**Choosing Copies**: Query: Does duplication need independence (deep) or equivalence (shallow/no-copy)? Align explicitly with equality (M01C05):
- For value-like types, `copy(x) == x` should normally hold, regardless of shallow vs deep.
- For entity-like types, you must decide whether `copy(x)` is “the same logical entity” (`copy(x) == x`) or a distinct one (`copy(x) != x`) and design both equality and copy hooks accordingly.

Interaction with Hazards: Copies break aliases; custom `__deepcopy__` implementations that ignore `memo` risk infinite recursion on cyclic graphs.

## 4. Practical Guidelines

- **Default to Module**: Use `copy.copy` for shallow; `copy.deepcopy` for deep—but be explicit about *why* you need a copy. Prefer shallow for containers where shared elements are intentional; prefer deep only where independence of nested state is part of the contract.
- **Custom Discipline**: Implement `__copy__` for entity semantics (e.g. new identity, shared or reset counters); implement `__deepcopy__` with `memo` for aggregates that need controlled duplication of nested state. For resource-owning types (files, sockets, DB sessions, locks), either:
  - explicitly raise `TypeError` from `__copy__`/`__deepcopy__`, or
  - implement a very narrow snapshot behaviour and document it aggressively.
- **Smell Detection**: Audit where copies are happening: if most copies exist purely to paper over unexpected mutations from other parts of the system, redesign the ownership and mutability story instead of piling on more copying.
- **Cycle Safety**: Leverage memo in `__deepcopy__`; test with cyclic graphs (e.g., self-referential lists).
- **Testing Fidelity**:
  - For value-like types, assert `copy(x) == x` and, if you intend to allocate a new object, also assert `copy(x) is not x`.
  - For entity-like types, assert whatever you decided in the design section (either `copy(x) == x` or `copy(x) != x`), and be explicit about whether identity (`is`) changes.
  - In all cases where you expect independence, verify that mutating the copy does not affect the original (for deep copies of mutable aggregates).

**Impacts on Design and Sharing**:
- **Design**: Tailored semantics decouple from aliases; smells prompt refactoring to ownership.
- **Sharing**: Copies enable safe replication; misuse amplifies GC pressure.

## Exercises for Mastery

1. Implement shallow `__copy__` for a `Point` value; verify equality but distinct identity post-copy.
2. Add deep `__deepcopy__` to a `Graph` aggregate with cycles; test memo breaks recursion and mutations isolate.
3. Refactor a sharing-heavy `Cache` to minimize copies via immutability; profile before/after and identify smells.

This core empowers replication without excess. Next, M01C08 surveys the data model as design surface.
