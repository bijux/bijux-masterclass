# Copying and Versioning of Objects and Aggregates Over Time

## Purpose

Design how objects are copied, snapshotted, and evolved without corrupting meaning.

Copy semantics matter when:
- you snapshot state for debugging or audit,
- you clone drafts into active objects,
- you version persisted aggregates across deployments.

## Where This Fits

Running example: a monitoring service that fetches metrics, evaluates rules, and emits alerts. In earlier modules we refactored toward a layered design (domain/application/infrastructure) with explicit roles. From M03 onward, we tighten *data integrity* and *lifecycle semantics* so the system stays correct under change.

## 1. Copying: Shallow vs Deep Is a Policy Choice

Python provides:
- `copy.copy` (shallow)
- `copy.deepcopy` (deep)

Neither is “correct” universally.

Design rule:
- define what copying means for your domain objects.

For immutable value objects, copying is often unnecessary.
For aggregates with mutable collections, copying can be essential for snapshots.

## 2. Snapshotting Aggregates

A snapshot is a read-only view of state at a point in time.

Options:
- deep copy the aggregate (can be expensive),
- build a separate immutable snapshot dataclass,
- serialize to a stable representation (dict/JSON) for audit.

Prefer explicit snapshot representations for clarity and teachability.

## 3. Version Fields and Compatibility

If you persist aggregates, add a version marker:

- schema version for serialized data,
- aggregate version for optimistic concurrency.

Versioning tells you how to interpret old data and how to migrate it (M05C49).

## 4. Clone Semantics for Lifecycle Transitions

When activating a draft, you often *derive* an active rule from it.

That’s a copy with enrichment:
- carries metric/threshold,
- adds identity and timestamps.

This is a domain-level copy semantics, best encoded as a method:
- `DraftRule.activate(...) -> ActiveRule` (M03C28).

## 5. Tests: Copy and Snapshot Must Preserve Invariants

Write tests that prove:
- snapshots don’t change when the live object changes (if that is required),
- cloning preserves semantic fields correctly,
- version markers are included in serialized forms.

## Practical Guidelines

- Define copy semantics explicitly; don’t rely on `deepcopy` as a default policy.
- Prefer explicit snapshot types for audit/debug views over copying whole object graphs blindly.
- Include version markers in persisted/serialized forms.
- Encode lifecycle clones as domain methods that preserve invariants (Draft → Active).

## Exercises for Mastery

1. Implement an immutable snapshot of your aggregate and prove it doesn’t change when the live aggregate mutates.
2. Add a schema version field to your serialized rule representation and write a test.
3. Write a clone method that enriches an object (copy + new fields) and test its invariants.
