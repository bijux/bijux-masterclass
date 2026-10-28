# Checkpoint — Module 08: Security in the Public Contract

## Required result

Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures.

## Demonstrate

- Model API-key and bearer security schemes.
- Read AND/OR semantics in security requirements correctly.
- Use global security and operation overrides deliberately.
- Separate authentication, authorization, and ownership.
- Document security failures without leaking implementation details.

## Commands

```bash
make -C capstone security-test
make -C capstone python-test
make -C capstone typescript
make -C capstone python-live
make -C capstone typescript-live
make -C capstone capability-report
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Security in the Public Contract** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Security in the Public Contract**
- focused result for: Model API-key and bearer security schemes.
- public, durable, security, or operational observation showing: Every operation has an explicit security decision and cross-owner artifact access is rejected.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Security in the Public Contract**
- a limitation statement naming every live dependency required to support the strongest **Security in the Public Contract** claim but not exercised

## Defend the design

1. Answer the central question: **How does the contract state who may call an operation and what failures clients can observe without pretending that documentation enforces policy?**
2. Demonstrate this capstone result: Every operation has an explicit security decision and cross-owner artifact access is rejected.
3. Show the **Security in the Public Contract** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Every operation has an explicit security decision and cross-owner artifact access is rejected.—all focused checks pass, the **Security in the Public Contract** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
