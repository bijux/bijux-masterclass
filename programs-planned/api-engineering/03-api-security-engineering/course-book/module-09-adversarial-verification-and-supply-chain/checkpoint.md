# Checkpoint — Module 09: Adversarial Verification and Supply-Chain Assurance

## Required result

Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.

## Demonstrate

- Trace tests to threats and requirements.
- Remove or mutate controls and confirm the proof fails.
- Use shared hostile vectors across languages.
- Pin direct and transitive dependencies and produce an SBOM.
- Interpret scanner output instead of treating tools as authorities.

## Commands

```bash
make module-proof MODULE=09 TRACK=python
make module-proof MODULE=09 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **How do we know a security check detects a missing control rather than merely confirming the control is present?**
2. Demonstrate this capstone result: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.—all focused checks pass, the **Adversarial Verification and Supply-Chain Assurance** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
