# Checkpoint — Module 02: Type System, Nullability, and Semantic Modeling

## Required result

Release Analysis Graph API 1.0 type and nullability policies.

## Demonstrate

- [ ] Design types around client concepts.
- [ ] Choose nullability from failure guarantees.
- [ ] Model lists, interfaces, unions, enums, scalars, and inputs.
- [ ] Apply oneof input semantics.
- [ ] Detect schema promises the runtime cannot keep.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-02-type-nullability.json` containing the released and scratch type declarations, completed data trees, error paths, bubble targets, and OneOf coercion table. Include a short design decision explaining why the released nullability is sustainable across authorization and source failure.

## Defend the design

1. Answer the central question in one paragraph: How does the schema make useful promises without promising values the runtime cannot sustain?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Type System, Nullability, and Semantic Modeling** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
