# Checkpoint — Module 09: Cloud Primitives, Identity, and Failure Domains

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Publish provider-neutral compute, identity, network, storage, DNS, load-balancing, metadata, quota, and failure-domain requirements for Course 2.**;
- all evidence named in the module lab;
- the planted defect `SYS-09` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Publish provider-neutral compute, identity, network, storage, DNS, load-balancing, metadata, quota, and failure-domain requirements for Course 2.

## Oral defense

Answer without notes:

> Which cloud resources and trust boundaries are required to preserve the host guarantees without copying one provider’s vocabulary into the architecture?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
