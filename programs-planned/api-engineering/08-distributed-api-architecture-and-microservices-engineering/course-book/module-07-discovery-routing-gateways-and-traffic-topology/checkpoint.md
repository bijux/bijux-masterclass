# Checkpoint — Discovery, Routing, Gateways, and Traffic Topology

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/dependency-graph.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-07-routing-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/architecture/adr/0006-gateway-owns-no-business-state.md` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do callers find healthy service instances and route traffic without moving business ownership into gateways or creating several competing retry layers?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Routing proof passes and a failed canary rolls back to a compatible authoritative path.
