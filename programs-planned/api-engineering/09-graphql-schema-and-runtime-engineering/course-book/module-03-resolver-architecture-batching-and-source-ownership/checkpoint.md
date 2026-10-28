# Checkpoint — Module 03: Resolver Architecture, Batching, and Source Ownership

## Required result

Replace N+1 nested calls with request-scoped batching.

## Demonstrate

- [ ] Map every field to one source.
- [ ] Construct request-scoped context.
- [ ] Explain and measure n+1.
- [ ] Implement batch loaders.
- [ ] Divide deadlines and observe fan-out.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-03-batching.json` with parent count, field occurrences, unique keys, dispatch count, source calls, maximum batch size, tenant partition, cancellation outcome, and cache scope. Include both the naïve and repaired results.

## Defend the design

1. Answer the central question in one paragraph: How can nested graph execution remain faithful to service ownership without producing N+1 calls?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Resolver Architecture, Batching, and Source Ownership** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
