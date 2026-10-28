# Checkpoint — Channels, Health, Discovery, Load Balancing, and Lifecycle

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/lifecycle.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/operations/service-config.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-08-lifecycle-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do clients and servers manage long-lived channels, instance health, name resolution, load balancing, startup, draining, and shutdown without hiding failure or losing active work?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

Channels, servers, health, reconnect, and shutdown must have bounded explicit lifecycles, and no correctness property may depend on one server's process memory.

Record the result in your learning journal before proceeding.
