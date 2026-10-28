# Checkpoint — Module 01: Threat Modeling and Security Requirements

## Required result

The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.

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

## Defend the design

1. Answer the central question: **What must be protected, from whom, across which boundaries, and how will we know the protection works?**
2. Demonstrate this capstone result: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: every accepted threat names an asset, boundary, security requirement, control owner, test, and residual risk.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.—all focused checks pass, the **Threat Modeling and Security Requirements** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
