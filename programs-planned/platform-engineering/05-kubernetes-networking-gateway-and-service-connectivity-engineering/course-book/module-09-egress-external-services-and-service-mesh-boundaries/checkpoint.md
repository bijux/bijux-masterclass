# Checkpoint — Egress and mesh boundaries

## Required evidence

- external dependency catalogue
- egress path and NAT capacity model
- DNS/peer/redirect validation policy
- private endpoint evidence plan
- service mesh requirement decision
- completed egress lab

## Decision defense

Defend why hostname allowlisting, NetworkPolicy, and service-mesh mTLS are complementary rather than interchangeable controls.

## Progression gate

Progress only when the evidence is reproducible and your explanation separates desired policy, selected endpoints, programmed data plane, and observed protocol behavior.
