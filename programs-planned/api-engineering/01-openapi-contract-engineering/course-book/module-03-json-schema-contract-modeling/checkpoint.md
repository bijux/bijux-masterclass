# Checkpoint — Module 03: JSON Schema Contract Modeling

## Required result

Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.

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

## Defend the design

1. Answer the central question: **Which JSON values are legal, and which invalid states must the contract make impossible?**
2. Demonstrate this capstone result: Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.—all focused checks pass, the **JSON Schema Contract Modeling** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
