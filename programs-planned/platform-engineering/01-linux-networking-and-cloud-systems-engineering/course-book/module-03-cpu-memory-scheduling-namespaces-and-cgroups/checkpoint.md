# Checkpoint — Module 03: CPU, Memory, Scheduling, Namespaces, and cgroups

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Publish and exercise a resource envelope for Atlas using cgroup v2 and systemd resource controls, with explicit throttling and memory-failure behavior.**;
- all evidence named in the module lab;
- the planted defect `SYS-03` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Publish and exercise a resource envelope for Atlas using cgroup v2 and systemd resource controls, with explicit throttling and memory-failure behavior.

## Oral defense

Answer without notes:

> How does the kernel share finite host resources, and how can one workload be bounded without making false isolation claims?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
