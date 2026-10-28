# Checkpoint — Module 02: Service Boundaries, Bounded Contexts, and Contract Ownership

## Required result

Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control.

## Demonstrate

- [ ] Identify capabilities, invariants, and ubiquitous language that belong together.
- [ ] Separate business-service ownership from gateway, worker, and platform components.
- [ ] Assign one accountable owner to every public http operation, event, rpc, and data set.
- [ ] Reject shared libraries that secretly preserve cross-service domain coupling.
- [ ] Design anti-corruption mappings between service-specific models.
- [ ] Recognize distributed-monolith boundaries before implementation begins.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/service-catalog.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/architecture/data-ownership.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-02-ownership-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Service Boundaries, Bounded Contexts, and Contract Ownership** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
