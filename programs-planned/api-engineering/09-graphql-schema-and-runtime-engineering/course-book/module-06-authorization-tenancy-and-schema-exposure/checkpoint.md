# Checkpoint — Module 06: Authorization, Tenancy, and Schema Exposure

## Required result

Prove field, tenant, collection, and sensitive-output authorization.

## Demonstrate

- [ ] Enforce field and tenant authorization.
- [ ] Filter collections at the source.
- [ ] Protect sensitive output fields.
- [ ] Delegate state-dependent policy.
- [ ] Choose an introspection and trusted-document policy.

## Commands

```bash
make core-proof
```

## Evidence to retain

Create `reports/module-06-authorization.json` with principal class, tenant, operation, field coordinate, decision, concealment behavior, source-call count, cache key class, and subscription closure reason. Pseudonymize subject and object identities.

## Defend the design

1. Answer the central question in one paragraph: How can clients select flexible fields without gaining flexible authority?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Authorization, Tenancy, and Schema Exposure** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
