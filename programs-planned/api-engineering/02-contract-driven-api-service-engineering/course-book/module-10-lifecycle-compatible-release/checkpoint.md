# Checkpoint — Module 10: Lifecycle and Compatible Release

## Required result

Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof.

## Demonstrate

- Distinguish startup, liveness, readiness, and draining.
- Order application and schema releases safely.
- Keep old and new service versions compatible during expansion.
- Define the rollback boundary explicitly.
- Release API 1.2 without breaking API 1.1 consumers.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=10 TRACK=python
make module-proof MODULE=10 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Lifecycle and Compatible Release** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Lifecycle and Compatible Release**
- focused result for: Distinguish startup, liveness, readiness, and draining.
- public, durable, security, or operational observation showing: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **compatible service and schema release**
- a limitation statement naming every live dependency required to support the strongest **Lifecycle and Compatible Release** claim but not exercised

## Defend the design

1. Answer the central question: **Can the service start, migrate, coexist, drain, roll back, and recover without violating its public contract or data?**
2. Demonstrate this capstone result: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.
3. Show the **Lifecycle and Compatible Release** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior.
5. State which environment-backed **Lifecycle and Compatible Release** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.—all focused checks pass, the **Lifecycle and Compatible Release** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
