# Worked answers — Graph Interface Placement and the Operation Lifecycle

Compare the decision rule and evidence, not just wording.

## 1. Why is a graph edge not permission to join two private databases?

The edge describes a client relationship, while data ownership remains with services. A private join bypasses service authorization, versioning, and operational policy. The decisive evidence is the field-source map plus a call trace showing service APIs rather than database connections.

**Decisive evidence.** Trace `Query.project` through the ownership catalogue and loopback call log. The claim is falsified by any gateway database client, cross-service SQL, or business-state table.

## 2. Classify invalid JSON, an unknown field, and Artifact Service timeout by phase.

Invalid JSON is HTTP framing; an unknown field is GraphQL validation; the timeout is execution. This classification controls status, response shape, metrics, and retry policy.

**Decisive evidence.** Send one malformed JSON request, one valid JSON document with an unknown field, and one request during an Artifact Service outage. Verify phase, status, data shape, and source-call count separately.

## 3. Why must operationName select exactly one operation when a document contains several?

Execution must be unambiguous. Without an operation name, the server cannot know which variable definitions and selection set to execute. The request is rejected before execution.

**Decisive evidence.** Execute a document containing two named operations without `operationName`, then with each valid name and with an unknown name. Only the two explicit valid selections may enter execution.

## 4. May GET execute a mutation because the GraphQL document is valid?

No. GET has safe-method semantics and may be cached or prefetched. The course HTTP profile allows GET only for query operations and returns 405 for mutation or subscription execution.

**Decisive evidence.** Run the transport profile against a mutation sent by GET. The request must be rejected before the mutation resolver and Analysis Control call counters remain unchanged.

## 5. What does validation prove that parsing does not?

Parsing proves the document follows grammar. Validation proves selections, arguments, variables, fragments, and operation structure are legal for the released schema.

**Decisive evidence.** Use a syntactically valid operation that selects an unknown field. Parsing must succeed, schema validation must fail, and no admission or source-execution record may exist.

## 6. Why is cost admission separate from GraphQL validation?

A valid query can still be too deep, broad, or expensive. Admission applies service-specific resource policy after standard validity and before execution.

**Decisive evidence.** Use a schema-valid alias storm and an oversized `first` variable. Cost admission must reject both after validation but before any downstream span or call.

## 7. Who owns Query.project and who owns its graph shape?

Analysis Control owns project facts; the graph team owns the client-facing field definition and composition policy, reviewed with Analysis Control.

**Decisive evidence.** Compare `resolver-ownership.yaml`, the SDL `@source` directive, and the call trace. Analysis Control must supply the fact while the graph release owns only its exposed shape.

## 8. What is wrong with returning HTTP 500 for every GraphQL error?

It erases request versus execution phases, misleads intermediaries, and prevents useful partial data. Stable GraphQL responses should carry structured errors while true host failures remain HTTP failures.

**Decisive evidence.** Exercise malformed input, validation failure, nullable downstream failure, and host crash. The HTTP and GraphQL response profiles must distinguish all four rather than collapse them into status 500.

## 9. Why is the GraphQL over HTTP source labeled draft?

Its current page identifies Stage 2. The course may profile it, but cannot present draft provisions as a finalized standard.

**Decisive evidence.** Pin the course claim to the official GraphQL over HTTP page and record its maturity label. A change in that published label would require updating the course profile.

## 10. How can a resolver create a new architecture edge?

Adding a downstream service call changes synchronous depth, deadline division, availability, security, and tracing. It requires dependency-graph review.

**Decisive evidence.** Add a resolver call in a scratch dependency graph and recalculate synchronous depth, deadline allocation, source fan-out, and failure surface. The architecture review must observe the new edge.

## 11. What evidence proves the gateway owns no business state?

The data-ownership map, graph metadata migrations, resolver call trace, and absence of project/run/artifact tables in the gateway database.

**Decisive evidence.** Inspect gateway migrations, source imports, and a complete operation trace. Only schema, client, budget, and resume metadata may persist locally; business facts must remain service-owned.

## 12. When should a capability remain an HTTP endpoint rather than enter GraphQL?

When it is streaming bytes, has clear cache and status semantics, or gains no client-composition value. Artifact download remains an authorized URL rather than binary GraphQL payload.

**Decisive evidence.** Compare a large authorized artifact transfer through GraphQL and the existing HTTP download capability. Keep HTTP when graph composition adds no value and worsens streaming, caching, or range semantics.
