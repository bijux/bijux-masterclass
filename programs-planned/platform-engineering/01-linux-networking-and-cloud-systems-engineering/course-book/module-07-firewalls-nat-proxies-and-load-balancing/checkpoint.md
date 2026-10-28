# Checkpoint — Module 07: Firewalls, NAT, Proxies, and Load Balancing

## Evidence to retain

- a baseline transcript from before the module change;
- the exact configuration, code, or architecture diff implementing: **Place Atlas behind a bounded reverse proxy, define host firewall policy, remove untrusted forwarding headers, and demonstrate health-aware backend removal.**;
- all evidence named in the module lab;
- the planted defect `SYS-07` failing for the predicted reason;
- the focused regression after repair;
- an evidence-class statement naming every stronger claim not executed.

## Demonstration

Demonstrate this result:

> Place Atlas behind a bounded reverse proxy, define host firewall policy, remove untrusted forwarding headers, and demonstrate health-aware backend removal.

## Oral defense

Answer without notes:

> Which intermediary is allowed to accept, transform, route, or reject traffic, and which identity survives each hop?

Then explain the owner, transition, failure boundary, and decisive oracle for the capstone mechanism.

## Progression decision

Continue only when the lab cleanup is verified, the Atlas baseline passes again, and you can defend why the repair did not weaken an earlier course boundary.
