# Lab — Module 09: Adversarial Verification and Supply-Chain Assurance

> **Module 09:** Adversarial Verification and Supply-Chain Assurance

## Objective

Assemble the complete adversarial proof ladder. Execute at least six planted defects, minimize failures, generate dependency/SBOM evidence with available tools, triage a fixture vulnerability, and prove private fixture material is absent from release staging.

## Why this lab matters

This lab turns the module’s governing question—**How do adversarial tests and supply-chain evidence show that controls fail closed and that the proof is sensitive?**—into a falsifiable experiment. The final proof ladder links threat, requirement, code, negative vector, mutant sensitivity, dependency evidence, and residual limitation. That is stronger than a long list of tools because it explains which security property each result supports.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build hostile vectors, negative policy tests, planted vulnerabilities, dependency evidence, SBOM/provenance routes, and scanner disposition**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we know a security check detects a missing control rather than merely confirming the control is present?*

## Hypothesis

The clean implementation should satisfy this claim: **shared adversarial vectors; planted-defect sensitivity; deterministic reports; core/full proof separation; dependency pins and lock policy; SBOM/provenance route; secret scan coverage; finding disposition record.** When the lab introduces this fault—**Implement and test: Remove or mutate controls and confirm the proof fails**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Implement and test: Trace tests to threats and requirements.
2. Implement and test: Remove or mutate controls and confirm the proof fails.
3. Implement and test: Use shared hostile vectors across languages.
4. Implement and test: Pin direct and transitive dependencies and produce an SBOM.
5. Implement and test: Interpret scanner output instead of treating tools as authorities.

### Required planted defect

Remove or bypass the central control for **Adversarial Verification and Supply-Chain Assurance** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Implement and test: Remove or mutate controls and confirm the proof fails**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Assemble the complete adversarial proof ladder. Execute at least six planted defects, minimize failures, generate dependency/SBOM evidence with available tools, triage a fixture vulnerability, and prove private fixture material is absent from release staging**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- shared adversarial vectors
- planted-defect sensitivity
- deterministic reports
- core/full proof separation
- dependency pins and lock policy
- SBOM/provenance route
- secret scan coverage
- finding disposition record

## Required evidence

- baseline transcript proving the previous checkpoint before **Adversarial Verification and Supply-Chain Assurance** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Adversarial Verification and Supply-Chain Assurance**
- focused result for: Trace tests to threats and requirements.
- public, durable, security, or operational observation showing: Ten planted vulnerabilities are detected, repaired, and retained as regressions; supply-chain evidence becomes reproducible.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **adversarial and supply-chain verification**
- a limitation statement naming every live dependency required to support the strongest **Adversarial Verification and Supply-Chain Assurance** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Adversarial Verification and Supply-Chain Assurance**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Implement and test: Remove or mutate controls and confirm the proof fails** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Adversarial Verification and Supply-Chain Assurance**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Adversarial Verification and Supply-Chain Assurance** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Adversarial Verification and Supply-Chain Assurance**. A green command without the negative case and causal explanation does not satisfy this gate.
