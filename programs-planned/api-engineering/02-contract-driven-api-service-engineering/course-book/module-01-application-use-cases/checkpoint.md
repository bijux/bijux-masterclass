# Checkpoint — Module 01: Application Use Cases and Boundaries

## Required result

Project operations run through framework-independent use cases while preserving the Course 1 contract.

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

## Defend the design

1. Answer the central question: **How does a public operation become maintainable application behavior without making route handlers the architecture?**
2. Demonstrate this capstone result: Project operations run through framework-independent use cases while preserving the Course 1 contract.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: route adapters translate HTTP input into application commands; use cases own decisions.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Project operations run through framework-independent use cases while preserving the Course 1 contract.—all focused checks pass, the **Application Use Cases and Boundaries** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
