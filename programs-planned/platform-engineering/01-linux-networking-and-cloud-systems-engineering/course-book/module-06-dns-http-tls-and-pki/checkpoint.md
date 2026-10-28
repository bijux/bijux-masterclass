# Checkpoint — Module 06: DNS, HTTP, TLS, and PKI

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Serve Atlas through an HTTPS edge with a local trust chain, correct names, certificate verification, rotation evidence, and protocol-aware health checks.**;
- all evidence named in the module lab;
- the planted defect `SYS-06` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Serve Atlas through an HTTPS edge with a local trust chain, correct names, certificate verification, rotation evidence, and protocol-aware health checks.

## Oral defense

Answer without notes:

> How does a client turn a name into an authenticated application connection, and where can that chain fail?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
