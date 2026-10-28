# Checkpoint — Module 08: Virtualization, Images, Boot, and Cloud Compute

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Define the Atlas machine image, boot sequence, cloud-init inputs, ephemeral-disk policy, metadata access, maintenance behavior, and replacement strategy.**;
- all evidence named in the module lab;
- the planted defect `SYS-08` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Define the Atlas machine image, boot sequence, cloud-init inputs, ephemeral-disk policy, metadata access, maintenance behavior, and replacement strategy.

## Oral defense

Answer without notes:

> What changes—and what does not—when the Linux host becomes a virtual machine created from an image?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
