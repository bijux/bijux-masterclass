# Checkpoint — Module 01: Processes, System Calls, Files, and Signals

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Run the Atlas API and worker as separate processes with explicit descriptors, exit behavior, signal handling, and observable process ownership.**;
- all evidence named in the module lab;
- the planted defect `SYS-01` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Run the Atlas API and worker as separate processes with explicit descriptors, exit behavior, signal handling, and observable process ownership.

## Oral defense

Answer without notes:

> How does a Linux process actually acquire resources, communicate, fail, and terminate?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
