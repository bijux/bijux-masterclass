# Checkpoint — object concurrency and lifecycle

## Required evidence

- field-ownership map;
- rejected conflict transcript;
- finalizer cleanup transcript;
- condition with current observedGeneration;
- owner-reference graph.

## Decision defense

Defend one deliberate ownership transfer and one field that must never be force-owned by the Atlas controller.

## Progression gate

Proceed only when concurrent changes, child lifecycle, and deletion obligations are all explicit.
