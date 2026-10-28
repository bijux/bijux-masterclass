# Worked Answers — Module 01: Graph Interface Placement and the Operation Lifecycle

Use these solutions to audit your reasoning for **Graph Interface Placement and the Operation Lifecycle**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a graph edge not permission to join two private databases?

The edge describes a client relationship, while data ownership remains with services. A private join bypasses service authorization, versioning, and operational policy. The decisive evidence is the field-source map plus a call trace showing service APIs rather than database connections.

**Decisive evidence.** Trace `Query.project` through the ownership catalogue and loopback call log. The claim is falsified by any gateway database client, cross-service SQL, or business-state table.

The chapter’s decisive distinction is this: This distinction prevents a common architectural regression. A team sees a graph edge from AnalysisRun to Artifact and concludes that the gateway may issue a SQL join across two databases. The graph edge is a client-facing relationship; its resolver is an authorized service call or a controlled projection. Schema topology and storage topology are deliberately different.

## 2. Classify invalid JSON, an unknown field, and Artifact Service timeout by phase.

Invalid JSON is HTTP framing; an unknown field is GraphQL validation; the timeout is execution. This classification controls status, response shape, metrics, and retry policy.

**Decisive evidence.** Send one malformed JSON request, one valid JSON document with an unknown field, and one request during an Artifact Service outage. Verify phase, status, data shape, and source-call count separately.

In the cumulative capstone, the rule becomes concrete: Errors must be assigned to the phase that discovered them. Invalid JSON is an HTTP framing problem. An unknown field is a GraphQL validation problem. A missing artifact permission is an execution authorization problem. Artifact Service unavailability is a path-specific execution error. Collapsing all failures into HTTP 500 makes clients, gateways, and operators unable to distinguish invalid demand from platform failure.

## 3. Why must operationName select exactly one operation when a document contains several?

Execution must be unambiguous. Without an operation name, the server cannot know which variable definitions and selection set to execute. The request is rejected before execution.

**Decisive evidence.** Execute a document containing two named operations without `operationName`, then with each valid name and with an unknown name. Only the two explicit valid selections may enter execution.

A useful way to reason about the boundary is: A document can contain multiple named operations and reusable fragments. The server must select exactly one operation when several are present. Variables are coerced against declared input types before execution. Validation checks the selected fields against the schema and applies rules such as fragment definition, leaf selection, variable compatibility, and subscription root constraints.

## 4. May GET execute a mutation because the GraphQL document is valid?

No. GET has safe-method semantics and may be cached or prefetched. The course HTTP profile allows GET only for query operations and returns 405 for mutation or subscription execution.

**Decisive evidence.** Run the transport profile against a mutation sent by GET. The request must be rejected before the mutation resolver and Analysis Control call counters remain unchanged.

The implementation consequence is: The GraphQL core specification is transport-agnostic. The course HTTP profile accepts POST with JSON and requires clients to advertise application/graphql-response+json. GET is allowed only for query operations because mutations have side effects. A well-formed HTTP request may still contain a GraphQL document that fails parsing or validation.

## 5. What does validation prove that parsing does not?

Parsing proves the document follows grammar. Validation proves selections, arguments, variables, fragments, and operation structure are legal for the released schema.

**Decisive evidence.** Use a syntactically valid operation that selects an unknown field. Parsing must succeed, schema validation must fail, and no admission or source-execution record may exist.

The important nuance is: A GraphQL request passes through identifiable phases: HTTP framing, document acquisition, parsing, operation selection, validation, variable coercion, admission policy, execution, value completion, and response serialization. Authentication and request context are established before field execution; field authorization remains part of execution because different selections can have different permissions.

## 6. Why is cost admission separate from GraphQL validation?

A valid query can still be too deep, broad, or expensive. Admission applies service-specific resource policy after standard validity and before execution.

**Decisive evidence.** Use a schema-valid alias storm and an oversized `first` variable. Cost admission must reject both after validation but before any downstream span or call.

Under concurrency or failure, the distinction becomes: The table prevents two damaging shortcuts. First, a resolver must never run during parsing, validation, or admission. A malformed or unaffordable document must not cause a source-service call. Second, an execution failure must not be reported as a validation failure merely because both appear in an errors array. Operational telemetry, client retry behavior, and security review all depend on the phase being truthful.

## 7. Who owns Query.project and who owns its graph shape?

Analysis Control owns project facts; the graph team owns the client-facing field definition and composition policy, reviewed with Analysis Control.

**Decisive evidence.** Compare `resolver-ownership.yaml`, the SDL `@source` directive, and the call trace. Analysis Control must supply the fact while the graph release owns only its exposed shape.

The design remains honest only if: GraphQL describes the capabilities clients may select; it does not declare that every object is stored as one record or owned by the graph gateway. In the Analysis Platform, Project and AnalysisRun are graph types because clients reason about them together, but their facts remain owned by Analysis Control. Artifact belongs to Artifact Service. DeliverySummary is an eventually consistent view owned by Notification Service.

## 8. What is wrong with returning HTTP 500 for every GraphQL error?

It erases request versus execution phases, misleads intermediaries, and prevents useful partial data. Stable GraphQL responses should carry structured errors while true host failures remain HTTP failures.

**Decisive evidence.** Exercise malformed input, validation failure, nullable downstream failure, and host crash. The HTTP and GraphQL response profiles must distinguish all four rather than collapse them into status 500.

The consumer-facing consequence is: Status handling follows the draft profile carefully: non-GraphQL middleware failures remain normal HTTP failures, while a GraphQL response uses the GraphQL response media type and contains data, errors, or both. The course records that the source specification is Stage 2 and avoids presenting draft flexibility as a permanent guarantee.

## 9. Why is the GraphQL over HTTP source labeled draft?

Its current page identifies Stage 2. The course may profile it, but cannot present draft provisions as a finalized standard.

**Decisive evidence.** Pin the course claim to the official GraphQL over HTTP page and record its maturity label. A change in that published label would require updating the course profile.

The operational consequence is: Status handling follows the draft profile carefully: non-GraphQL middleware failures remain normal HTTP failures, while a GraphQL response uses the GraphQL response media type and contains data, errors, or both. The course records that the source specification is Stage 2 and avoids presenting draft flexibility as a permanent guarantee.

## 10. How can a resolver create a new architecture edge?

Adding a downstream service call changes synchronous depth, deadline division, availability, security, and tracing. It requires dependency-graph review.

**Decisive evidence.** Add a resolver call in a scratch dependency graph and recalculate synchronous depth, deadline allocation, source fan-out, and failure surface. The architecture review must observe the new edge.

The strongest engineering interpretation is: The dependency graph from Course 8 remains active. A new resolver that adds a third synchronous hop or a cycle is an architecture change, not merely a schema change. Field review therefore includes source authority and fan-out evidence.

## 11. What evidence proves the gateway owns no business state?

The data-ownership map, graph metadata migrations, resolver call trace, and absence of project/run/artifact tables in the gateway database.

**Decisive evidence.** Inspect gateway migrations, source imports, and a complete operation trace. Only schema, client, budget, and resume metadata may persist locally; business facts must remain service-owned.

The defect-oriented view is: The decisive lab evidence is not a screenshot of a GraphQL IDE. It is a phase trace showing that rejected operations made zero source calls, a call trace showing source ownership, and a response proving the declared partial-failure behavior.

## 12. When should a capability remain an HTTP endpoint rather than enter GraphQL?

When it is streaming bytes, has clear cache and status semantics, or gains no client-composition value. Artifact download remains an authorized URL rather than binary GraphQL payload.

**Decisive evidence.** Compare a large authorized artifact transfer through GraphQL and the existing HTTP download capability. Keep HTTP when graph composition adds no value and worsens streaming, caching, or range semantics.

Across the Python and TypeScript tracks, the invariant is: The capstone therefore returns an authorized artifact download URL rather than embedding binary content in GraphQL. The graph can expose metadata and a capability; the byte transfer remains an HTTP operation owned by Artifact Service. This is not an inconsistency. It is correct interface selection.
