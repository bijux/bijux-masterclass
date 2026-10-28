# Checkpoint — Module 01: Application Use Cases and Boundaries

## Required result

Create transport, application, and adapter boundaries for the fixed operation ledger.

## Demonstrate

- Separate transport, application, domain, and infrastructure responsibilities.
- Translate public models into internal commands and results.
- Inject clocks, identifiers, and external dependencies.
- Keep business decisions out of FastAPI and Fastify handlers.
- Map every operation ID to one application owner.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=01 TRACK=python
make module-proof MODULE=01 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Application Use Cases and Boundaries** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Application Use Cases and Boundaries**
- focused result for: Separate transport, application, domain, and infrastructure responsibilities.
- public, durable, security, or operational observation showing: Project operations run through framework-independent use cases while preserving the Course 1 contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **operation-to-use-case mapping**
- a limitation statement naming every live dependency required to support the strongest **Application Use Cases and Boundaries** claim but not exercised

## Defend the design

1. Answer the central question: **How does a public operation become maintainable application behavior without making route handlers the architecture?**
2. Demonstrate this capstone result: Project operations run through framework-independent use cases while preserving the Course 1 contract.
3. Show the **Application Use Cases and Boundaries** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: route adapters translate HTTP input into application commands; use cases own decisions.
5. State which environment-backed **Application Use Cases and Boundaries** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Project operations run through framework-independent use cases while preserving the Course 1 contract.—all focused checks pass, the **Application Use Cases and Boundaries** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
