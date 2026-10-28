# Checkpoint — Multi-platform truth

## Required evidence

- amd64 and arm64 binaries;
- ELF/linkage inspection;
- deterministic two-platform index;
- per-platform evidence matrix;
- rejected mislabelled candidate;
- explicit native/cross/emulated classification.

## Decision defense

Defend the choice to ship one multi-platform release rather than separate product versions. State the condition that would reverse the decision.

## Progression gate

Proceed when the release subject is an exact digest and every platform-specific child has verified executable truth. Module 6 will move these immutable objects through a registry without allowing mutable tags to become authority.

## Continue

- [Next stage](../module-06-registries-distribution-digests-tags-and-referrers/index.md)
- [Course index](../index.md)
