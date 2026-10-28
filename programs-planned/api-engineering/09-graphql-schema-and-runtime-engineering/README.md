# Course 9 — GraphQL Schema and Runtime Engineering

GraphQL is not a replacement for service ownership. It is a typed graph
interface through which clients select capabilities while the runtime preserves
authorization, demand limits, batching, consistency, and the boundaries of the
services beneath it.

This course continues the same Analysis Runs Platform used throughout the API
Engineering program. By the end of Course 8, the platform already has a public
HTTP/OpenAPI interface, durable services, adversarial security controls,
reliability evidence, performance budgets, asynchronous event contracts, typed
RPC, and deliberately extracted service boundaries. Course 9 adds a governed
graph-access layer without allowing the graph gateway to become a second domain
model, an ownerless integration service, or a cross-service database join
engine.

## What the learner builds

The cumulative capstone is **Analysis Graph API 1.0**. It exposes project, run,
artifact, delivery, search, mutation, node-lookup, and subscription capabilities
through one schema while preserving the authority of Analysis Control, Artifact
Service, and Notification Service.

The learner implements and proves:

- a schema with deliberate nullability, interfaces, unions, and OneOf input;
- stable global identifiers and tenant-bound, signed high-water cursors;
- exact persisted-operation admission;
- request-scoped batching without cross-request cache leakage;
- owner-aware resolver and field policy;
- idempotent mutations and expected-version concurrency;
- cost, depth, alias, list-size, and service-fan-out budgets;
- partial responses with precise error paths and truthful nulls;
- resumable subscriptions with duplicate suppression and gap detection;
- schema and active-operation compatibility gates;
- a real loopback composition laboratory over separate HTTP processes;
- an exact publication handoff for Course 10.

## Reader-first structure

The authoritative product is [`course-book/`](course-book/index.md). Every
numbered module has one complete chapter, one set of transfer exercises, matching
worked answers, one controlled laboratory, and one evidence checkpoint. The
capstone and proof routes make the book's claims executable; they do not replace
the explanation.

Course 1 used Python and TypeScript symmetrically to establish that a public
contract is language-independent. Course 9 follows the later program strategy:
choose one primary implementation track and use the other as a comparative
reference. Externally relevant semantics must match; framework syntax and
internal architecture do not need artificial one-to-one duplication.

## Course sequence

1. Graph interface placement and operation lifecycle
2. Type system, nullability, and semantic modeling
3. Resolver architecture, batching, and source ownership
4. Queries, identifiers, connections, and pagination
5. Mutations, idempotency, concurrency, and domain results
6. Authorization, tenancy, and schema exposure
7. Demand control, persisted operations, and caching
8. Errors, partial data, consistency, and observability
9. Subscriptions, resume, and incremental delivery
10. Schema evolution, federation, governance, and final defense

## Start

From the course root:

```bash
make help
make doctor
make predecessor-proof
make capstone-tour
make core-proof
make manifest-proof
```

Then begin with [`course-book/start-here.md`](course-book/start-here.md).
The normal study route is ten dense teaching days plus orientation and final
defense. A checkpoint is passed by evidence, not by reading completion.

## Evidence discipline

Dependency-light proofs validate the exact semantic mechanisms shipped in this
repository. Optional framework and external-tool routes are separately labeled.
The bounded teaching parser and executor are never represented as a complete
GraphQL implementation. Read [`PRODUCTION-CLAIMS.md`](PRODUCTION-CLAIMS.md) for
the exact executed and environment-backed evidence boundary.
