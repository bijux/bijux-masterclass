# Checkpoint — Synchronous Collaboration, API Composition, and Dependency Budgets

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/dependency-graph.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-dependency-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-04-partial-response.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

Dependency proof passes and the completed-run response distinguishes unavailable artifacts from zero artifacts.
