# Checkpoint — Module 09: Evolution, Compatibility, and Audience Views

## Required result

Create compatible and rejected release candidates, compatibility gates, and public/partner audience views.

## Demonstrate

- Analyze compatibility in the correct message direction.
- Treat requiredness, enums, media types, statuses, and operation IDs as consumer commitments.
- Design deprecation and major-version migration.
- Apply Overlay documents deterministically.
- Block incompatible minor releases in CI.

## Commands

```bash
make -C capstone releases
make -C capstone diff
make -C capstone oasdiff
make -C capstone overlays
make -C capstone clients-generate
make -C capstone verify-report
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Evolution, Compatibility, and Audience Views** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Evolution, Compatibility, and Audience Views**
- focused result for: Analyze compatibility in the correct message direction.
- public, durable, security, or operational observation showing: API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Evolution, Compatibility, and Audience Views**
- a limitation statement naming every live dependency required to support the strongest **Evolution, Compatibility, and Audience Views** claim but not exercised

## Defend the design

1. Answer the central question: **How can a published API change without silently breaking existing consumers?**
2. Demonstrate this capstone result: API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.
3. Show the **Evolution, Compatibility, and Audience Views** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.—all focused checks pass, the **Evolution, Compatibility, and Audience Views** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
