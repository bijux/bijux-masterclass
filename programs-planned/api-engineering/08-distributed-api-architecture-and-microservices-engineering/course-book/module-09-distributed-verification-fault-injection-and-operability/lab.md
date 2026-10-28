# Lab — Prove that the architecture tests can fail

> **Module 09:** Distributed Verification, Fault Injection, and Operability

## Objective

Execute distributed schedule tests and reject all ten planted architecture defects.

## Why this lab matters

This lab turns the module’s governing question—**How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures?**—into a falsifiable experiment. Both tracks run shared semantic vectors and independent unit tests. The course tool separately verifies architecture YAML, service-owned migrations, release candidates, and planted defects. The optional Compose/Kubernetes routes are classified as environment-backed rather than silently simulated.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the proof ladder, critical journey, release matrix, service catalog, and planted defects.

## Hypothesis

The clean implementation should satisfy this claim: **All legitimate schedules converge or produce explicit manual findings; every planted defect fails the intended gate; cleanup restores the baseline.** When the lab introduces this fault—**Inject after-commit response loss in artifact storage and reconcile by stable effect identity**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run service-local and shared-vector suites as a baseline.
2. Inject after-commit response loss in artifact storage and reconcile by stable effect identity.
3. Inject a projection gap and prove the affected view stops claiming completeness.
4. Run each planted defect through its assigned rejecting proof.
5. Run `make network-lab-proof` to exercise five independent processes and a real connection failure.
6. Extend `reports/module-09-fault-plan.yaml` with one PostgreSQL- or container-backed fault for your environment, including abort and cleanup conditions.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject after-commit response loss in artifact storage and reconcile by stable effect identity**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Execute distributed schedule tests and reject all ten planted architecture defects**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

All legitimate schedules converge or produce explicit manual findings; every planted defect fails the intended gate; cleanup restores the baseline.

## Required evidence

- `capstone/planted-defects/`
- `reports/module-09-distributed-proof.json`
- `reports/module-09-fault-plan.yaml`
- the machine-readable output of `make network-lab-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Distributed Verification, Fault Injection, and Operability**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject after-commit response loss in artifact storage and reconcile by stable effect identity** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove mutants, reset fault schedules, clear generated state, and rerun baseline proofs.

## Completion gate

Ten defects are rejected and the post-clean baseline plus reconciliation proof passes.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Distributed Verification, Fault Injection, and Operability**. A green command without the negative case and causal explanation does not satisfy this gate.
