# Checkpoint — Module 04: Storage, Filesystems, I/O, and Durability

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Separate Atlas runtime, configuration, logs, queue state, and results; publish files atomically; and prove disk-full and restart behavior.**;
- all evidence named in the module lab;
- the planted defect `SYS-04` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Separate Atlas runtime, configuration, logs, queue state, and results; publish files atomically; and prove disk-full and restart behavior.

## Oral defense

Answer without notes:

> When an application says that data was written, which bytes are actually durable and on which failure boundary?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
