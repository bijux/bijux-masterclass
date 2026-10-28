# Production claims and evidence boundary

This course teaches production-oriented distributed-system design, but it does not equate a local simulator or Compose topology with production proof.

## Executed dependency-light evidence

The release proof executes architecture policy, data ownership, dependency graph, saga, capability, version-skew, extraction, reconciliation, Python, and TypeScript tests without external infrastructure.

## Environment-backed evidence

The package includes explicit routes for multi-process containers, PostgreSQL service databases, NATS, Kubernetes, network policy, and strict documentation rendering. Those routes are only reported as executed when their dependencies are actually available.

## Claims the course refuses to make

- that microservices are inherently more mature than a modular monolith;
- that a service mesh supplies application authorization or transactional correctness;
- that eventual consistency means arbitrary inconsistency;
- that a saga is a distributed rollback transaction;
- that passing service-local tests proves the distributed outcome;
- that independent deployment exists when services share a database, release train, or private model.
