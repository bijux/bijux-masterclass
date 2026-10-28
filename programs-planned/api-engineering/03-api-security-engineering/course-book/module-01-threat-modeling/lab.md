# Lab — Module 01: Threat Modeling and Security Requirements

## Objective

Build the complete capstone security case from the actual data flow. Plant one orphan threat and one requirement with no proof, demonstrate that the checker fails, then repair both.


## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *What must be protected, from whom, across which boundaries, and how will we know the protection works?*

## Failure action and investigation

1. Freeze the baseline that currently provides: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
2. Construct the smallest local counterexample to: What must be protected, from whom, across which boundaries, and how will we know the protection works?
3. Implement and test the control needed to identify assets, actors, entry points, and trust boundaries.
4. Exercise the valid boundary and at least two hostile boundaries from the shared vectors.
5. Remove or bypass the central control and prove the predicted oracle fails.
6. Restore the control and verify trace every control to a threat, requirement, owner, and test.
7. Compare the secondary track through the shared security outcome.
8. Clean runtime state and retain only the minimized regression and named evidence.

### Required planted defect

Remove or bypass the central control for **Threat Modeling and Security Requirements** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: What must be protected, from whom, across which boundaries, and how will we know the protection works? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Threat Modeling and Security Requirements** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Identify assets, actors, entry points, and trust boundaries.
- public, durable, security, or operational observation showing: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **threat-to-control traceability**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Threat Modeling and Security Requirements**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=01`.
4. Confirm the system again provides this result: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.

## Completion gate

- Identify assets, actors, entry points, and trust boundaries.
- Write concrete abuse cases and security invariants.
- Use STRIDE as a prompt rather than a substitute for analysis.
- Rank risk with explicit assumptions.
- Trace every control to a threat, requirement, owner, and test.
