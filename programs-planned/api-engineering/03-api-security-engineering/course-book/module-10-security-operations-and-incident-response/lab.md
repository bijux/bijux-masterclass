# Lab — Module 10: Security Operations and Incident Response

## Objective

Run the combined compromise scenario: leaked webhook secret, suspected stolen token, cross-tenant artifact attempt, and vulnerable dependency. Detect, triage, contain, rotate/revoke, preserve evidence, release compatibly, rerun proofs, and update threats/residual risks.


## Setup conditions

The previous baseline is: **Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *When a credential, key, or dependency is compromised, how do we contain the event without destroying evidence or breaking the API?*

## Failure action and investigation

1. Implement and test: Design actionable security events and audit records.
2. Implement and test: Revoke tokens and API keys deliberately.
3. Implement and test: Rotate webhook and signing keys with overlap.
4. Implement and test: Preserve timelines and confidence levels.
5. Implement and test: Update threats, controls, and tests after the incident.

### Required planted defect

Remove or bypass the central control for **Security Operations and Incident Response** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: When a credential, key, or dependency is compromised, how do we contain the event without destroying evidence or breaking the API? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Security Operations and Incident Response** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Design actionable security events and audit records.
- public, durable, security, or operational observation showing: Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **security incident containment and recovery**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Security Operations and Incident Response**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=10`.
4. Confirm the system again provides this result: Course 3 ends with security profile 1.0, migrations 006–007, and a closed compromise exercise.

## Completion gate

- structured incident timeline
- token/API-key revocation
- webhook-key rotation
- evidence preservation
- compatible security release
- full proof rerun
- security-case update
- public-only outgoing handoff
