# Checkpoint — Module 01: Graph Interface Placement and the Operation Lifecycle

## Required result

Publish the graph boundary and operation-lifecycle trace.

## Demonstrate

- [ ] Place graphql without changing service authority.
- [ ] Trace parse, validate, admit, execute, complete, and serialize phases.
- [ ] Classify failures by phase.
- [ ] Apply the course http profile.
- [ ] Review a field as an architecture edge.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-01-operation-lifecycle.json` with:

```json
{
  "schemaRelease": "1.0.0",
  "cases": [
    {
      "name": "valid",
      "lastPhase": "serialization",
      "operationId": "...",
      "sourceCalls": {},
      "responseClass": "complete"
    }
  ]
}
```

Do not include bearer tokens, raw arbitrary variables, or returned business data. Include assertions showing which planted defect would make the report fail.

## Defend the design

1. Answer the central question in one paragraph: Where does GraphQL belong, and what happens between receiving a document and returning a response?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Graph Interface Placement and the Operation Lifecycle** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
