# Lab — Module 09: Adversarial Verification and Supply-Chain Assurance

## Objective

Assemble the complete adversarial proof ladder. Execute at least six planted defects, minimize failures, generate dependency/SBOM evidence with available tools, triage a fixture vulnerability, and prove private fixture material is absent from release staging.


## Setup conditions

The previous baseline is: **Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we know a security check detects a missing control rather than merely confirming the control is present?*

## Failure action and investigation

1. Implement and test: Trace tests to threats and requirements.
2. Implement and test: Remove or mutate controls and confirm the proof fails.
3. Implement and test: Use shared hostile vectors across languages.
4. Implement and test: Pin direct and transitive dependencies and produce an SBOM.
5. Implement and test: Interpret scanner output instead of treating tools as authorities.

### Required planted defect

Remove or bypass the central control for **Adversarial Verification and Supply-Chain Assurance** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: How do we know a security check detects a missing control rather than merely confirming the control is present? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Adversarial Verification and Supply-Chain Assurance** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Trace tests to threats and requirements.
- public, durable, security, or operational observation showing: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **adversarial and supply-chain verification**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Adversarial Verification and Supply-Chain Assurance**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=09`.
4. Confirm the system again provides this result: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.

## Completion gate

- shared adversarial vectors
- planted-defect sensitivity
- deterministic reports
- core/full proof separation
- dependency pins and lock policy
- SBOM/provenance route
- secret scan coverage
- finding disposition record
