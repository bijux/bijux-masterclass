# Lab — Module 01: Threat Modeling and Security Requirements

> **Module 01:** Threat Modeling and Security Requirements

## Objective

Build the complete capstone security case from the actual data flow. Plant one orphan threat and one requirement with no proof, demonstrate that the checker fails, then repair both.

## Why this lab matters

This lab turns the module’s governing question—**Which assets, actors, trust boundaries, abuse cases, and assumptions define the real security problem?**—into a falsifiable experiment. Version the security case with the service. Re-review it when an operation, credential type, trust boundary, dependency, data classification, administrative capability, or deployment route changes. A release diff should state which threats were added, retired, re-ranked, or left unchanged and which assumptions were invalidated. “No security impact” is a conclusion that needs evidence, not a default label.

It advances the cumulative Analysis Runs Platform by requiring this result: **Create a security case that traces threats to requirements, control owners, tests, and residual risk**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *What must be protected, from whom, across which boundaries, and how will we know the protection works?*

## Hypothesis

The clean implementation should satisfy this claim: **Identify assets, actors, entry points, and trust boundaries; Write concrete abuse cases and security invariants; Use STRIDE as a prompt rather than a substitute for analysis; Rank risk with explicit assumptions; Trace every control to a threat, requirement, owner, and test.** When the lab introduces this fault—**Remove or bypass the central control and prove the predicted oracle fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control and prove the predicted oracle fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build the complete capstone security case from the actual data flow. Plant one orphan threat and one requirement with no proof, demonstrate that the checker fails, then repair both**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- Identify assets, actors, entry points, and trust boundaries.
- Write concrete abuse cases and security invariants.
- Use STRIDE as a prompt rather than a substitute for analysis.
- Rank risk with explicit assumptions.
- Trace every control to a threat, requirement, owner, and test.

## Required evidence

- baseline transcript proving the previous checkpoint before **Threat Modeling and Security Requirements** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Threat Modeling and Security Requirements**
- focused result for: Identify assets, actors, entry points, and trust boundaries.
- public, durable, security, or operational observation showing: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **threat-to-control traceability**
- a limitation statement naming every live dependency required to support the strongest **Threat Modeling and Security Requirements** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Threat Modeling and Security Requirements**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control and prove the predicted oracle fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Threat Modeling and Security Requirements**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Threat Modeling and Security Requirements** experiment.
3. Rerun the focused regression and `make module-proof MODULE=01`.
4. Confirm the system again provides this result: The capstone gains a machine-readable threat catalog, security requirements, operation policies, and residual-risk record.

## Completion gate

- Identify assets, actors, entry points, and trust boundaries.
- Write concrete abuse cases and security invariants.
- Use STRIDE as a prompt rather than a substitute for analysis.
- Rank risk with explicit assumptions.
- Trace every control to a threat, requirement, owner, and test.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Threat Modeling and Security Requirements**. A green command without the negative case and causal explanation does not satisfy this gate.
