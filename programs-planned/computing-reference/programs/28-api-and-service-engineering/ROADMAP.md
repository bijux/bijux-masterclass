# 28. API & Service Engineering

**Program code:** `API`

**Purpose:** Develop end-to-end command of designing, implementing, securing, evolving, testing, and operating synchronous and asynchronous service interfaces.

**Level-II professional outcome:** Ready to build and lead production API and service work across HTTP/REST, RPC, GraphQL, events, gateways, contracts, security, reliability, and governance.

**Prerequisites:** software design; networking and HTTP basics; security foundations; distributed-systems foundations.

**Primary ownership:** HTTP semantics; resource and operation design; API contracts and schemas; REST, RPC, GraphQL, and event APIs; authentication and authorization at APIs; compatibility and versioning; resilience and performance; API testing and observability; gateways and service interaction; API governance and developer experience.

**Explicit exclusions:** overall software architecture (Program 12); general distributed algorithms (Program 27); platform product ownership (Program 29); network-layer engineering (Program 24).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — HTTP and Web Protocol Semantics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Resources, Representations, and Messages** | `001-resources-representations-and-messages.md` |
| 002 | **HTTP Methods and Their Semantics** | `002-http-methods-and-their-semantics.md` |
| 003 | **Status Codes and Error Meaning** | `003-status-codes-and-error-meaning.md` |
| 004 | **Headers and Metadata** | `004-headers-and-metadata.md` |
| 005 | **Content Negotiation** | `005-content-negotiation.md` |
| 006 | **Conditional Requests** | `006-conditional-requests.md` |
| 007 | **Caching** | `007-caching.md` |
| 008 | **Idempotency and Safety** | `008-idempotency-and-safety.md` |
| 009 | **HTTP/1.1, HTTP/2, and HTTP/3 Semantics** | `009-http-1-1-http-2-and-http-3-semantics.md` |
| 010 | **Tracing a Request Through Client, Proxy, and Service** | `010-tracing-a-request-through-client-proxy-and-service.md` |

### Block 02 — Resource and Operation Design

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Outside-In API Requirements** | `011-outside-in-api-requirements.md` |
| 012 | **Resource Identification** | `012-resource-identification.md` |
| 013 | **URI Design** | `013-uri-design.md` |
| 014 | **Collections and Individual Resources** | `014-collections-and-individual-resources.md` |
| 015 | **Create, Read, Update, and Delete Semantics** | `015-create-read-update-and-delete-semantics.md` |
| 016 | **Partial Updates** | `016-partial-updates.md` |
| 017 | **Filtering, Sorting, and Pagination** | `017-filtering-sorting-and-pagination.md` |
| 018 | **Long-Running Operations** | `018-long-running-operations.md` |
| 019 | **Bulk and Batch Operations** | `019-bulk-and-batch-operations.md` |
| 020 | **Designing an API from Consumer Tasks Rather Than Database Tables** | `020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md` |

### Block 03 — Contracts, Schemas, and Documentation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **API Contracts and Behavioral Guarantees** | `021-api-contracts-and-behavioral-guarantees.md` |
| 022 | **JSON Schema** | `022-json-schema.md` |
| 023 | **OpenAPI Structure** | `023-openapi-structure.md` |
| 024 | **Request and Response Modeling** | `024-request-and-response-modeling.md` |
| 025 | **Validation Constraints** | `025-validation-constraints.md` |
| 026 | **Reusable Schema Components** | `026-reusable-schema-components.md` |
| 027 | **Examples and Executable Documentation** | `027-examples-and-executable-documentation.md` |
| 028 | **Contract-First and Code-First Workflows** | `028-contract-first-and-code-first-workflows.md` |
| 029 | **Mocking and Consumer Exploration** | `029-mocking-and-consumer-exploration.md` |
| 030 | **Reviewing a Contract for Ambiguity and Incompleteness** | `030-reviewing-a-contract-for-ambiguity-and-incompleteness.md` |

### Block 04 — Service Implementation and Boundary Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Transport, Application, and Domain Boundaries** | `031-transport-application-and-domain-boundaries.md` |
| 032 | **Request Parsing and Validation** | `032-request-parsing-and-validation.md` |
| 033 | **Authentication Context Propagation** | `033-authentication-context-propagation.md` |
| 034 | **Authorization Checks** | `034-authorization-checks.md` |
| 035 | **Error Translation** | `035-error-translation.md` |
| 036 | **Request-Scoped Transaction Boundaries** | `036-request-scoped-transaction-boundaries.md` |
| 037 | **Idempotency Keys** | `037-idempotency-keys.md` |
| 038 | **Concurrency Control at the API Boundary** | `038-concurrency-control-at-the-api-boundary.md` |
| 039 | **Rate Limits and Quotas** | `039-rate-limits-and-quotas.md` |
| 040 | **Implementing a Predictable Service Endpoint** | `040-implementing-a-predictable-service-endpoint.md` |

### Block 05 — API Security and Abuse Resistance

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **API Threat Modeling** | `041-api-threat-modeling.md` |
| 042 | **Credential and Token Handling** | `042-credential-and-token-handling.md` |
| 043 | **OAuth Authorization Flows** | `043-oauth-authorization-flows.md` |
| 044 | **Applying OpenID Connect at API Boundaries** | `044-applying-openid-connect-at-api-boundaries.md` |
| 045 | **Scope and Permission Design** | `045-scope-and-permission-design.md` |
| 046 | **Object-Level Authorization** | `046-object-level-authorization.md` |
| 047 | **Mass Assignment and Overposting** | `047-mass-assignment-and-overposting.md` |
| 048 | **Enumeration and Data Exposure** | `048-enumeration-and-data-exposure.md` |
| 049 | **Replay and Request Signing** | `049-replay-and-request-signing.md` |
| 050 | **Designing an API Against Expected Abuse Cases** | `050-designing-an-api-against-expected-abuse-cases.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — RPC, GraphQL, and Alternative Interface Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Remote Procedure Call Semantics** | `051-remote-procedure-call-semantics.md` |
| 052 | **Protocol Buffers and Schema Evolution** | `052-protocol-buffers-and-schema-evolution.md` |
| 053 | **Unary and Streaming gRPC** | `053-unary-and-streaming-grpc.md` |
| 054 | **Deadlines, Cancellation, and Metadata** | `054-deadlines-cancellation-and-metadata.md` |
| 055 | **GraphQL Schema Design** | `055-graphql-schema-design.md` |
| 056 | **GraphQL Execution, Resolvers, and Batching** | `056-graphql-execution-resolvers-and-batching.md` |
| 057 | **GraphQL Pagination and Incremental Delivery** | `057-graphql-pagination-and-incremental-delivery.md` |
| 058 | **GraphQL Authorization and Cost Control** | `058-graphql-authorization-and-cost-control.md` |
| 059 | **Webhooks, Server-Sent Events, and WebSockets** | `059-webhooks-server-sent-events-and-websockets.md` |
| 060 | **Choosing an Interface Style from Interaction Semantics** | `060-choosing-an-interface-style-from-interaction-semantics.md` |

### Block 07 — Event and Asynchronous APIs

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Commands, Events, and Messages** | `061-commands-events-and-messages.md` |
| 062 | **Event Schema Design** | `062-event-schema-design.md` |
| 063 | **AsyncAPI Contracts** | `063-asyncapi-contracts.md` |
| 064 | **Topic and Channel Design** | `064-topic-and-channel-design.md` |
| 065 | **Ordering and Partition Keys** | `065-ordering-and-partition-keys.md` |
| 066 | **Delivery and Acknowledgment** | `066-delivery-and-acknowledgment.md` |
| 067 | **Idempotent Consumers** | `067-idempotent-consumers.md` |
| 068 | **Dead-Letter Handling** | `068-dead-letter-handling.md` |
| 069 | **Event Versioning** | `069-event-versioning.md` |
| 070 | **Designing an Asynchronous API for Replay and Evolution** | `070-designing-an-asynchronous-api-for-replay-and-evolution.md` |

### Block 08 — Reliability, Performance, and Distributed Behavior

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Timeout and Deadline Budgets** | `071-timeout-and-deadline-budgets.md` |
| 072 | **Retries and Backoff** | `072-retries-and-backoff.md` |
| 073 | **Circuit Breaking and Bulkheads** | `073-circuit-breaking-and-bulkheads.md` |
| 074 | **API-Level Load Shedding** | `074-api-level-load-shedding.md` |
| 075 | **Backpressure Across Service Boundaries** | `075-backpressure-across-service-boundaries.md` |
| 076 | **API Caching and Invalidation** | `076-api-caching-and-invalidation.md` |
| 077 | **Fan-Out and Tail Latency** | `077-fan-out-and-tail-latency.md` |
| 078 | **Partial Results and Graceful Degradation** | `078-partial-results-and-graceful-degradation.md` |
| 079 | **Consistency and Read-After-Write Expectations** | `079-consistency-and-read-after-write-expectations.md` |
| 080 | **Preventing Failure Amplification Across Service Calls** | `080-preventing-failure-amplification-across-service-calls.md` |

### Block 09 — Lifecycle, Compatibility, and Governance

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Backward and Forward Compatibility** | `081-backward-and-forward-compatibility.md` |
| 082 | **Additive and Breaking Changes** | `082-additive-and-breaking-changes.md` |
| 083 | **Versioning Strategies** | `083-versioning-strategies.md` |
| 084 | **Deprecation and Sunset** | `084-deprecation-and-sunset.md` |
| 085 | **Consumer Inventory and Usage Evidence** | `085-consumer-inventory-and-usage-evidence.md` |
| 086 | **API Style Guides** | `086-api-style-guides.md` |
| 087 | **Design Reviews** | `087-design-reviews.md` |
| 088 | **Schema Registries and Contract Governance** | `088-schema-registries-and-contract-governance.md` |
| 089 | **API Product Ownership** | `089-api-product-ownership.md` |
| 090 | **Evolving an API Without Coordinated Consumer Releases** | `090-evolving-an-api-without-coordinated-consumer-releases.md` |

### Block 10 — API Platforms, Testing, and Operations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **API Gateways and Edge Responsibilities** | `091-api-gateways-and-edge-responsibilities.md` |
| 092 | **Service Discovery and Routing** | `092-service-discovery-and-routing.md` |
| 093 | **Service Mesh Relationships** | `093-service-mesh-relationships.md` |
| 094 | **Contract Testing** | `094-contract-testing.md` |
| 095 | **Integration and End-to-End API Testing** | `095-integration-and-end-to-end-api-testing.md` |
| 096 | **Fuzzing and Robustness Testing** | `096-fuzzing-and-robustness-testing.md` |
| 097 | **API Metrics, Logs, and Traces** | `097-api-metrics-logs-and-traces.md` |
| 098 | **Latency and Capacity Testing** | `098-latency-and-capacity-testing.md` |
| 099 | **Developer Portals and Onboarding** | `099-developer-portals-and-onboarding.md` |
| 100 | **Conducting a Production API and Service Readiness Review** | `100-conducting-a-production-api-and-service-readiness-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
