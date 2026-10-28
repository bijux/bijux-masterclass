# Checkpoint — Module 04: Queries, Identifiers, Connections, and Pagination

## Required result

Implement global IDs and stable, bound connections.

## Demonstrate

- [ ] Design meaningful roots.
- [ ] Encode and validate global identifiers.
- [ ] Implement stable connection pagination.
- [ ] Bind cursors to tenant and filters.
- [ ] Bound polymorphic search.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-04-connections.json` with the two traversal identities, page ID lists, high-water values, sort tuples, rejection reasons, and source rows examined. Hash sensitive identifiers in the report if necessary.

## Defend the design

1. Answer the central question in one paragraph: How can clients navigate lists and relationships without unstable pages, leaked internals, or unbounded work?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Queries, Identifiers, Connections, and Pagination** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
