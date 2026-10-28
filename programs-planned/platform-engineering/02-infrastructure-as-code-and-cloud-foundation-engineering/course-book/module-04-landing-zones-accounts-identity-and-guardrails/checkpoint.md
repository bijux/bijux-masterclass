# Checkpoint — Landing-Zone Authority

## Required evidence

Retain:

- account and organizational-unit graph;
- owner and account-lifecycle table;
- workforce, CI plan, CI apply, workload, audit, security, and break-glass identity matrix;
- plan/apply separation record;
- audit-archive authority decision;
- organization-guardrail scope and limitation;
- region-policy exception review;
- quota and budget ownership;
- compromised-workload blast-radius analysis;
- rejected unsafe landing-zone fixtures.

## Decision defense

For a compromised Atlas runtime session, name the exact accounts and resources it can affect. Explain why it cannot change organization policy or delete authoritative audit evidence, and identify which workload-local controls are still required despite account separation.

## Progression gate

You pass only when every organization-wide authority has a named owner, no workload runs in the management account, and no tag or folder name is mistaken for an access-control boundary.
