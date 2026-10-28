# Checkpoint — Build graph and reproducibility

## Required evidence

- effective context inventory;
- normalized build-input record;
- cache-dependency experiment;
- controlled rebuild digest comparison;
- secret-mount proof;
- rejected secret-layer candidate;
- scoped reproducibility statement.

## Decision defense

Defend the chosen multi-stage boundary and name one debugging convenience intentionally excluded from the runtime image.

## Progression gate

Proceed when target platform is an explicit build input and the release can prove its executable was not inherited from a cache built for another architecture.

## Continue

- [Next stage](../module-05-multi-platform-images-abi-and-architecture-truth/index.md)
- [Course index](../index.md)
