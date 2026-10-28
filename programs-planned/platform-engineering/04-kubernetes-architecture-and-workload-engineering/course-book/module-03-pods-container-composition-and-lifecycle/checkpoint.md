# Checkpoint — Pod lifecycle contract

## Required evidence

- Atlas API and worker Pod-template review;
- digest and security-context proof;
- writable-path classification;
- restart/replacement/termination transcript;
- declared evidence boundary for runtime enforcement.

## Decision defense

Defend every container in the Pod and every writable mount. Remove anything that lacks a shared-fate or data-class justification.

## Progression gate

Proceed only when Pod composition, retry behavior, and graceful shutdown preserve the Course 3 contract.
