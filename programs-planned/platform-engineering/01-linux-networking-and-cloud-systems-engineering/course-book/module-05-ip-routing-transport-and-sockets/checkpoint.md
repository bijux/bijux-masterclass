# Checkpoint — Module 05: IP, Routing, Transport, and Sockets

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Define Atlas listening addresses, route assumptions, port ownership, timeouts, and dual-stack behavior; prove them with socket and packet-path evidence.**;
- all evidence named in the module lab;
- the planted defect `SYS-05` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Define Atlas listening addresses, route assumptions, port ownership, timeouts, and dual-stack behavior; prove them with socket and packet-path evidence.

## Oral defense

Answer without notes:

> How does a byte leave one process and reach the intended process across interfaces, routes, and transport state?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
