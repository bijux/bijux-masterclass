# Checkpoint — Module 09: Generation, Testing, Reflection, and Schema Governance

## Required result

Publish a reproducible generation pipeline, checked descriptor inventory, generated-client build matrix, runtime catalogue comparison, and Course 7 RPC release gate.

## Demonstrate

- [ ] Define authoritative proto source and reproducible generation inputs.
- [ ] Use `protoc` and buf as complementary generation, lint, and compatibility tools.
- [ ] Build and inspect descriptor sets and runtime reflection inventories.
- [ ] Separate semantic unit tests, in-process protocol tests, network conformance, and generated-client tests.
- [ ] Detect generated-code drift and unsupported tool capabilities.
- [ ] Govern services, methods, owners, consumers, versions, and deprecation through an rpc catalogue.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/contracts/descriptors/analysis-v1.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/rpc-case/rpc-catalog.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-09-governance-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we make proto source, generated code, runtime services, tests, descriptors, reflection, and release policy agree without treating code generation as proof?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Generation, Testing, Reflection, and Schema Governance** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
