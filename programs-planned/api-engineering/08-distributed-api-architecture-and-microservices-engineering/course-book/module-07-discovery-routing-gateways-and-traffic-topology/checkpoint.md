# Checkpoint — Module 07: Discovery, Routing, Gateways, and Traffic Topology

## Required result

Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision.

## Demonstrate

- [ ] Distinguish service identity from instance address and endpoint health.
- [ ] Compare dns, registry, client-side, proxy, and platform routing models.
- [ ] Keep authentication normalization and protocol adaptation at the edge while preserving domain ownership.
- [ ] Avoid business workflows and private data stores inside the gateway.
- [ ] Design canary, shadow, and failover routes with bounded blast radius.
- [ ] Evaluate service mesh features without making the mesh the source of application correctness.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/dependency-graph.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-07-routing-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/architecture/adr/0006-gateway-owns-no-business-state.md` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do callers find healthy service instances and route traffic without moving business ownership into gateways or creating several competing retry layers?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Discovery, Routing, Gateways, and Traffic Topology** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
