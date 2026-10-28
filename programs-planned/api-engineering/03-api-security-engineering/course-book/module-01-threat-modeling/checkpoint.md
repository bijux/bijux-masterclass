# Checkpoint — Module 01: Threat Modeling and Security Requirements

## Required result

Create a security case that traces threats to requirements, control owners, tests, and residual risk.

## Demonstrate

- Identify assets, actors, entry points, and trust boundaries.
- Write concrete abuse cases and security invariants.
- Use STRIDE as a prompt rather than a substitute for analysis.
- Rank risk with explicit assumptions.
- Trace every control to a threat, requirement, owner, and test.

## Commands

```bash
make module-proof MODULE=01 TRACK=python
make module-proof MODULE=01 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Threat Modeling and Security Requirements** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Threat Modeling and Security Requirements**
- focused result for: Identify assets, actors, entry points, and trust boundaries.
- public, durable, security, or operational observation showing: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **threat-to-control traceability**
- a limitation statement naming every live dependency required to support the strongest **Threat Modeling and Security Requirements** claim but not exercised

## Defend the design

1. Answer the central question: **What must be protected, from whom, across which boundaries, and how will we know the protection works?**
2. Demonstrate this capstone result: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
3. Show the **Threat Modeling and Security Requirements** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk.
5. State which environment-backed **Threat Modeling and Security Requirements** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.—all focused checks pass, the **Threat Modeling and Security Requirements** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
