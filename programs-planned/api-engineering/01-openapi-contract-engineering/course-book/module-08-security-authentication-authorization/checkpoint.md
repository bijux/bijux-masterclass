# Checkpoint — Module 08: Security in the Public Contract

## Required result

Every operation has an explicit security decision and cross-owner artifact access is rejected.

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

## Defend the design

1. Answer the central question: **How does the contract state who may call an operation and what failures clients can observe without pretending that documentation enforces policy?**
2. Demonstrate this capstone result: Every operation has an explicit security decision and cross-owner artifact access is rejected.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Every operation has an explicit security decision and cross-owner artifact access is rejected.—all focused checks pass, the **Security in the Public Contract** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
