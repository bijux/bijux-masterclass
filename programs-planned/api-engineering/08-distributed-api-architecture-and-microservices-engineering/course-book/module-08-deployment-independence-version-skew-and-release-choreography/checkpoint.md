# Checkpoint — Module 08: Deployment Independence, Version Skew, and Release Choreography

## Required result

Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence.

## Demonstrate

- [ ] Distinguish independent deployment from independent change and ownership.
- [ ] Model provider and consumer compatibility across http, events, and grpc.
- [ ] Design expand, migrate, observe, and contract release sequences.
- [ ] Support bounded version skew without permanent multi-version complexity.
- [ ] Use shadow and canary evidence before route cutover.
- [ ] Define rollback boundaries when data or messages have already changed.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/release-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/architecture/version-ledger.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-08-release-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Deployment Independence, Version Skew, and Release Choreography** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
