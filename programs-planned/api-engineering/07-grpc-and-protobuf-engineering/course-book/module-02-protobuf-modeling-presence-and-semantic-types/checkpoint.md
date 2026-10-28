# Checkpoint — Module 02: Protobuf Modeling, Presence, and Semantic Types

## Required result

Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior.

## Demonstrate

- [ ] Design request and response messages around application decisions rather than persistence records.
- [ ] Distinguish absent, present-with-default, empty, unknown, and inapplicable values.
- [ ] Use enum zero values, `optional`, `oneof`, repeated fields, maps, and semantic wrappers deliberately.
- [ ] Model resource names, request identifiers, correlation identifiers, revisions, and lease generations as different concepts.
- [ ] Protect 64-bit integer meaning across python, javascript, binary protobuf, and protojson.
- [ ] Maintain a proto3 executable baseline while understanding the editions 2024 frontier without pretending universal tool support.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/presence.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/shared/vectors/int64.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-02-model-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we encode domain meaning in Protobuf without allowing language defaults, JSON conventions, or storage models to erase important distinctions?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Protobuf Modeling, Presence, and Semantic Types** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
