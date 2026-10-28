# Checkpoint — Module 06: Golden Paths, Templates, and Self-Service Provisioning

## Required result

Publish and verify the `api-capability-v1` golden path and generated reference fixture.

## Demonstrate

- [ ] Design a golden path as a maintained product.
- [ ] Choose safe defaults and essential parameters.
- [ ] Render deterministically and atomically.
- [ ] Include ownership, tests, docs, and governance hooks.
- [ ] Govern upgrades and supported escape hatches.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-06-golden-path.json` with template version, parameters,
file digests, rejected defects, and upgrade classification.

## Defend the design

1. Answer the central question in one paragraph: How can a platform reduce repeated setup work without hiding essential engineering decisions or creating clone-and-forget debt?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Golden Paths, Templates, and Self-Service Provisioning** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
