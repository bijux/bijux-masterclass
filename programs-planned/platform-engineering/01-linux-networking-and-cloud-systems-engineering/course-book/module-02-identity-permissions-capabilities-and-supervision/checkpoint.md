# Checkpoint — Module 02: Identity, Permissions, Capabilities, and Service Supervision

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Give Atlas dedicated service identities, owned directories, restrictive modes, hardened systemd units, and unambiguous restart and shutdown policy.**;
- all evidence named in the module lab;
- the planted defect `SYS-02` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Give Atlas dedicated service identities, owned directories, restrictive modes, hardened systemd units, and unambiguous restart and shutdown policy.

## Oral defense

Answer without notes:

> Which authority should each process possess, and who is responsible for keeping it running?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
