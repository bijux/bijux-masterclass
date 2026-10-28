# Checkpoint — KRM and render integrity

## Required evidence

- Three deterministic environment render digests.
- An approved-field-path policy for overlays.
- A rendered identity and deletion report.
- Rejected mutable-source and selector-mutation cases.

## Decision defense

- Defend the base/overlay responsibility boundary.
- Explain canonicalization exclusions.
- Explain the field-ownership migration rule.

## Progression gate

Advance only when a reviewer can reconstruct the exact desired resource set without executing an undocumented input path.
