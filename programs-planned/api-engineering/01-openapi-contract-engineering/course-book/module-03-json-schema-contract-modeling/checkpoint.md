# Checkpoint — Module 03: JSON Schema Contract Modeling

## Required result

Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus.

## Demonstrate

- Distinguish missing, null, empty, and default.
- Constrain objects, arrays, strings, and numbers precisely.
- Use composition as logic rather than inheritance.
- Design tagged unions and separate input/output models.
- Verify a shared corpus of valid and invalid instances.

## Commands

```bash
make -C capstone examples
make -C capstone fixtures
make -C capstone python-test
make -C capstone typescript
make -C capstone core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **JSON Schema Contract Modeling** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **JSON Schema Contract Modeling**
- focused result for: Distinguish missing, null, empty, and default.
- public, durable, security, or operational observation showing: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **JSON Schema Contract Modeling**
- a limitation statement naming every live dependency required to support the strongest **JSON Schema Contract Modeling** claim but not exercised

## Defend the design

1. Answer the central question: **Which JSON values are legal, and which invalid states must the contract make impossible?**
2. Demonstrate this capstone result: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.
3. Show the **JSON Schema Contract Modeling** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.—all focused checks pass, the **JSON Schema Contract Modeling** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
