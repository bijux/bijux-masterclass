# Graph Interface Placement and the Operation Lifecycle

**Module 01 of 10**

> **Governing question:** Where does GraphQL belong, and what happens between receiving a document and returning a response?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 01 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- place GraphQL without changing service authority

- trace parse, validate, admit, execute, complete, and serialize phases

- classify failures by phase

- apply the course HTTP profile

- review a field as an architecture edge

## Capstone result

Publish the graph boundary and operation-lifecycle trace.

## GraphQL is a capability layer, not the data model

GraphQL describes the capabilities clients may select; it does not declare that every object is stored as one record or owned by the graph gateway. In the Analysis Platform, `Project` and `AnalysisRun` are graph types because clients reason about them together, but their facts remain owned by Analysis Control. `Artifact` belongs to Artifact Service. `DeliverySummary` is an eventually consistent view owned by Notification Service. The graph turns those capabilities into one typed selection language without creating a shared database.

This distinction prevents a common architectural regression. A team sees a graph edge from `AnalysisRun` to `Artifact` and concludes that the gateway may issue a SQL join across two databases. The graph edge is a client-facing relationship; its resolver is an authorized service call or a controlled projection. Schema topology and storage topology are deliberately different.

## The operation pipeline

A GraphQL request passes through identifiable phases: HTTP framing, document acquisition, parsing, operation selection, validation, variable coercion, admission policy, execution, value completion, and response serialization. Authentication and request context are established before field execution; field authorization remains part of execution because different selections can have different permissions.

Errors must be assigned to the phase that discovered them. Invalid JSON is an HTTP framing problem. An unknown field is a GraphQL validation problem. A missing artifact permission is an execution authorization problem. Artifact Service unavailability is a path-specific execution error. Collapsing all failures into HTTP 500 makes clients, gateways, and operators unable to distinguish invalid demand from platform failure.

## Queries are programs with a declared result shape

A document can contain multiple named operations and reusable fragments. The server must select exactly one operation when several are present. Variables are coerced against declared input types before execution. Validation checks the selected fields against the schema and applies rules such as fragment definition, leaf selection, variable compatibility, and subscription root constraints.

The course additionally applies admission rules for depth, aliases, cardinality, service fan-out, and trusted documents. Those are not replacements for GraphQL validation. A document can be valid and still too expensive or disallowed for a particular client.

## GraphQL over HTTP profile

The GraphQL core specification is transport-agnostic. The course HTTP profile accepts POST with JSON and requires clients to advertise `application/graphql-response+json`. GET is allowed only for query operations because mutations have side effects. A well-formed HTTP request may still contain a GraphQL document that fails parsing or validation.

Status handling follows the draft profile carefully: non-GraphQL middleware failures remain normal HTTP failures, while a GraphQL response uses the GraphQL response media type and contains `data`, `errors`, or both. The course records that the source specification is Stage 2 and avoids presenting draft flexibility as a permanent guarantee.

## Placement in the distributed platform

The gateway is an edge composition component. It may call Analysis Control and Artifact Service under one public request budget. It may read the versioned Notification summary with an explicit staleness field. It may not become a workflow owner, write source-service tables, or invent a mutation result before the owning service commits it.

The dependency graph from Course 8 remains active. A new resolver that adds a third synchronous hop or a cycle is an architecture change, not merely a schema change. Field review therefore includes source authority and fan-out evidence.

## A phase-by-phase execution model

Treat the GraphQL host as a pipeline with explicit ownership rather than a single `execute()` call. The distinction matters because each phase has different inputs, different failure semantics, and different evidence.

| Phase | Input | Successful result | Failure means | May call a business service? |
|---|---|---|---|---|
| HTTP framing | method, headers, body bytes | one transport request | the host cannot construct a GraphQL request | no |
| document acquisition | text or persisted-operation identifier | one exact document | the client requested an unknown or forbidden document | no |
| parsing | document text | syntax tree | the text is not GraphQL grammar | no |
| operation selection | syntax tree and `operationName` | one operation | execution would be ambiguous or missing | no |
| validation | operation and released schema | schema-valid operation | fields, fragments, variables, or selections are illegal | no |
| variable coercion | JSON variables and input types | typed values | client input cannot satisfy the declared types | no |
| admission | validated operation, identity, policy | accepted execution plan | valid demand exceeds trust or resource policy | no |
| execution | plan and request context | field values or execution errors | an authorized field source failed or rejected the request | yes |
| completion | field values and output types | typed response tree | a value violates its output type or non-null promise | no new source calls |
| serialization | completed tree | response bytes | the host cannot encode the result | no |

The table prevents two damaging shortcuts. First, a resolver must never run during parsing, validation, or admission. A malformed or unaffordable document must not cause a source-service call. Second, an execution failure must not be reported as a validation failure merely because both appear in an `errors` array. Operational telemetry, client retry behavior, and security review all depend on the phase being truthful.

A useful implementation exposes phase events even when a framework internally combines them. The capstone records `operation.lookup`, `operation.validate`, `operation.admit`, and `operation.execute` separately. Those events must use bounded attributes: operation identifier, client identity class, schema release, outcome, cost decision, and downstream service set. They must not record raw documents, bearer tokens, arbitrary variables, or returned data.

## Review every field as an architecture edge

A schema review that discusses only names and types is incomplete. For every non-trivial field, record the following seven facts:

1. **Coordinate** — for example, `AnalysisRun.artifacts`.
2. **Authority** — Artifact Service owns artifact facts.
3. **Resolver source** — a batched artifact-service call, not a database join.
4. **Authorization** — `ARTIFACT_READ` plus tenant and run relationship.
5. **Cardinality** — bounded by the source contract; no unbounded list.
6. **Consistency** — authoritative at read time, or explicitly stale if projected.
7. **Failure contract** — nullable field plus path-specific error when Artifact Service is unavailable.

This record turns schema review into architecture review. It reveals when a seemingly innocent field adds a remote hop, crosses a trust boundary, introduces a stale projection, or creates a list whose size the gateway cannot control. The `resolver-ownership.yaml` and field catalogue in the capstone are executable versions of this worksheet.

Consider adding `AnalysisRun.ownerEmail`. A schema-first discussion might ask whether the field should be `String!`. An engineering review asks who owns the email, whether the caller may see it, whether the value belongs in the graph at all, whether it creates a call to an identity service for every run, how it is cached, and what happens if the identity service is unavailable. A field can be syntactically elegant and architecturally wrong.

## Persisted operations and the operation lifecycle

The course supports governed persisted operations because they create a stable unit of review. A persisted identifier maps to exact normalized document bytes. The registry records the client, operation name, allowed variables, schema release, cost ceiling, and lifecycle state. Registration does not bypass parsing or validation; it moves those checks into a controlled release path and permits a faster runtime lookup.

Do not confuse a trusted-document allowlist with automatic persisted queries. APQ commonly uses a hash as a cache key and may permit a client to register an arbitrary document after a miss. A trusted registry is an admission boundary: only reviewed documents from declared clients become active. The same digest mechanism can support both, but the security and governance semantics differ.

The lifecycle is:

```text
client source document
        ↓ normalize and hash
review against schema, policy, and source ownership
        ↓
register as pending
        ↓ client release evidence
activate for named clients
        ↓ telemetry and deprecation
retire only after supported clients stop using it
```

A schema release cannot be judged from SDL alone. The release proof must revalidate all active operation documents and execute representative old operations against the candidate runtime. Conversely, retaining every operation forever is not a compatibility strategy; it prevents schema cleanup and hides abandoned clients. The registry needs ownership and retirement evidence.

## When GraphQL is the wrong interface

GraphQL is valuable when clients need several related typed capabilities in one request and different clients need different shapes. It is a poor default for every interaction.

Keep a capability outside GraphQL when one or more of these conditions dominate:

- the representation is a large byte stream, such as an artifact download;
- HTTP cache validators, range requests, and content negotiation are the primary protocol value;
- the command has one stable input and one stable output and gains no composition benefit;
- the operation is an administrative or bulk workflow with a separate trust boundary;
- the response must preserve precise HTTP status and header semantics;
- exposing selection flexibility would make cost or authorization harder without helping clients.

The capstone therefore returns an authorized artifact download URL rather than embedding binary content in GraphQL. The graph can expose metadata and a capability; the byte transfer remains an HTTP operation owned by Artifact Service. This is not an inconsistency. It is correct interface selection.

## An end-to-end request trace

For `GetProjectOverview`, the host performs this sequence:

```text
POST /graphql
  → authenticate caller and establish tenant context
  → resolve persisted digest to exact GetProjectOverview document
  → parse and select the named query
  → validate against Analysis Graph API 1.0
  → coerce projectId, first, and after
  → calculate field occurrences, cardinality multipliers, and service fan-out
  → authorize Query.project
  → call Analysis Control for project and one run page
  → batch artifact keys across returned runs
  → batch delivery-summary keys across returned runs
  → complete values under nullability rules
  → return data plus any path-specific errors
```

If Artifact Service fails, the project and runs can remain present because `AnalysisRun.artifacts` is nullable. Each affected path receives an error and the response declares partial completion. If Analysis Control fails while resolving the nullable `Query.project`, the field becomes null with an error. If `viewer` fails despite being non-null, null propagation can eliminate top-level data. These outcomes come from the schema contract, not ad hoc exception handling.

The decisive lab evidence is not a screenshot of a GraphQL IDE. It is a phase trace showing that rejected operations made zero source calls, a call trace showing source ownership, and a response proving the declared partial-failure behavior.

## Worked capstone review

Trace `GetProjectOverview`: the HTTP host resolves the persisted document, the parser builds the document, operation selection chooses one named query, validation checks schema use, admission computes cost and fan-out, execution calls Analysis Control and request-scoped loaders, completion applies nullability, and serialization emits data plus any path errors. At no point does the gateway query a service database.

## Python and TypeScript implications

Python and TypeScript both expose the operation phases as explicit functions. The optional frameworks provide complete parsers and executors; the dependency-light core makes admission and source calls inspectable. Neither framework is allowed to collapse phase-specific failures into one generic exception.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-01-*.json`; prose claims without its oracle do not pass.
