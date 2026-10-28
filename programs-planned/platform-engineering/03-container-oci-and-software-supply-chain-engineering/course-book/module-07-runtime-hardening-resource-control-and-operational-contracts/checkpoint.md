# Checkpoint — Runtime hardening

## Required evidence

- accepted API, worker, and probe profiles;
- effective identity/capability evidence;
- read-only-root and writable-mount proof;
- resource-bound declarations and evidence class;
- shutdown timeline;
- rejected unsafe profiles;
- secret/log leakage check.

## Decision defense

Defend every writable path and every retained capability. For Atlas, the expected capability list is empty; any exception needs measured evidence.

## Progression gate

Proceed when the image and runtime profile together satisfy the predecessor contract. Module 8 will inventory what the release contains and interpret vulnerability and license findings without treating scanner output as truth by itself.

## Continue

- [Next stage](../module-08-sboms-vulnerabilities-licenses-and-vex/index.md)
- [Course index](../index.md)
