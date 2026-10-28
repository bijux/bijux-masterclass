# Checkpoint — Module 09: Adversarial Verification and Supply-Chain Assurance

## Required result

Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Adversarial Verification and Supply-Chain Assurance** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Adversarial Verification and Supply-Chain Assurance**
- focused result for: Trace tests to threats and requirements.
- public, durable, security, or operational observation showing: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **adversarial and supply-chain verification**
- a limitation statement naming every live dependency required to support the strongest **Adversarial Verification and Supply-Chain Assurance** claim but not exercised

## Defend the design

1. Answer the central question: **How do we know a security check detects a missing control rather than merely confirming the control is present?**
2. Demonstrate this capstone result: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.
3. Show the **Adversarial Verification and Supply-Chain Assurance** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: negative vectors, mutants, locks, SBOM/provenance evidence, and vulnerability disposition prove controls and build inputs.
5. State which environment-backed **Adversarial Verification and Supply-Chain Assurance** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.—all focused checks pass, the **Adversarial Verification and Supply-Chain Assurance** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
