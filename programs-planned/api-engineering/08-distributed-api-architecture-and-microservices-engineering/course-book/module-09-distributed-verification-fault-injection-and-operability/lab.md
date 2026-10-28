# Lab — Prove that the architecture tests can fail

**Module:** Distributed Verification, Fault Injection, and Operability

## Objective

Execute distributed schedule tests and reject all ten planted architecture defects.

## Setup

Load the proof ladder, critical journey, release matrix, service catalog, and planted defects.

## Controlled actions

1. Run service-local and shared-vector suites as a baseline.
2. Inject after-commit response loss in artifact storage and reconcile by stable effect identity.
3. Inject a projection gap and prove the affected view stops claiming completeness.
4. Run each planted defect through its assigned rejecting proof.
5. Run `make network-lab-proof` to exercise five independent processes and a real connection failure.
6. Extend `reports/module-09-fault-plan.yaml` with one PostgreSQL- or container-backed fault for your environment, including abort and cleanup conditions.

## Correctness oracle

All legitimate schedules converge or produce explicit manual findings; every planted defect fails the intended gate; cleanup restores the baseline.

## Required evidence

- `capstone/planted-defects/`
- `reports/module-09-distributed-proof.json`
- `reports/module-09-fault-plan.yaml`
- the machine-readable output of `make network-lab-proof`

## Cleanup

Remove mutants, reset fault schedules, clear generated state, and rerun baseline proofs.

## Completion gate

Ten defects are rejected and the post-clean baseline plus reconciliation proof passes.

A successful command without the required evidence does not complete the lab.
