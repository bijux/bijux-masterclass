# Module 02 — Operations, Parameters, and Messages

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity?

## Where this module fits

Module 01 produced **Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior**. This module extends that result by asking: **How are parameters, request bodies, media types, status codes, and headers modeled without ambiguity?**

The new capstone increment is **Complete project and dataset messages, including pagination inputs, creation responses, and problem representations**. It becomes the prerequisite for **JSON Schema Contract Modeling**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Model path, query, header, cookie, and body input deliberately.
- Use request bodies and media types correctly.
- Describe response codes, headers, and representations as a complete outcome.
- Choose stable operation identifiers.
- Validate examples against their schemas.

## Capstone increment

Complete project and dataset messages, including pagination inputs, creation responses, and problem representations.

## Core model

### Driving question

> Where does each value belong, and how is it serialized?

### Observable outcome

Complete project and dataset operations with exact parameter locations, serialization, request bodies, response fields, status codes, and media types.

### 1. Location is part of meaning

`projectId` in a path identifies the target resource; `status` in a query refines a collection view; `If-Match` in a header makes the request conditional; a JSON property contributes to the submitted representation. Moving the same string between locations changes caching, routing, visibility, and compatibility.

Choose location from semantics before choosing framework syntax. A filter does not become a path segment because a router makes it easy. A concurrency precondition does not belong in the JSON patch because intermediaries and generic HTTP tooling understand the field-line semantics.
### 2. Parameter serialization is a wire algorithm

An OpenAPI Parameter Object describes more than a schema. `style`, `explode`, and `allowReserved` determine how arrays and objects become characters in a path, query string, header, or cookie. Two clients can agree that a value is `string[]` and still send incompatible wire forms.

Always pair a parameter schema with at least one literal URI or field-line example. For cursor pagination, `cursor=20` is simple. For arrays or objects, write the exact encoding and test the provider parser against it.
### 3. A request body is not a large parameter

Parameter Objects cover path, query, header, and cookie locations. Structured message content belongs under `requestBody`, with a content map keyed by media type. `requestBody.required` controls whether content must exist; schema `required` controls which object properties must exist once an object is present.

Confusing those two levels produces APIs that accidentally accept an absent body or demand optional fields. Tests need one case for no content and separate cases for missing properties.
### 4. Status, fields, and content form one response contract

A response is not only a JSON schema. `201` communicates creation, `204` forbids message content, `404` communicates target absence, and `415` says the submitted content format is unsupported. `Location`, `ETag`, and request-correlation fields can be required consumer inputs.

Document each meaningful branch. A broad `default` response cannot replace known statuses when consumers need distinct retry, correction, or authorization behavior.
### 5. Content negotiation has two directions

`Content-Type` describes content that is present. `Accept` expresses response preferences. A provider can reject unsupported request content with `415`, and can choose or reject a response representation based on `Accept`. OpenAPI content maps enumerate supported media types; they do not by themselves implement negotiation.

The capstone keeps success payloads JSON except the event stream and multipart upload introduced later. Problem responses use `application/problem+json`, which must be asserted independently from the success type.
### 6. Examples are executable claims

An example attached to a media type or schema is part of the published understanding of the operation. It must satisfy required fields, patterns, formats, union selection, and closure rules. A beautifully rendered invalid example trains consumers to send requests the schema rejects.

The course validates examples against the effective bundled schema and keeps invalid cases in a separate fixture corpus. Do not label invalid examples as normal request examples merely to demonstrate errors.

Complete this before editing YAML:

```text
resource or outcome:
request method and target:
request fields/content:
legal input set:
success response(s):
error response(s):
security decision:
state/retry/concurrency rule:
consumer compatibility commitment:
smallest counterexample:
proof command:
```

1. Place each value: project identifier, page limit, idempotency key, project patch, session token.
2. Write the wire form for a form/explode query array named `tag` with values `a` and `b`.
3. Distinguish `requestBody.required` from a schema `required` list.
4. Why must a 204 response omit a schema/content map?
5. Choose between 400, 404, 409, 412, 415, and 422 for: unknown resource, stale ETag, unsupported media type, invalid field, lifecycle conflict.

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Operations, Parameters, and HTTP Messages, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Path parameters are required and their names match template expressions. | OAS requirement | Routers and generators need a one-to-one mapping. | reference/structure checks |
| Parameter identity is the pair of `name` and `in`. | OAS model | A query and header parameter may share a name without being the same parameter. | bundle inspection |
| A response with status `204` has no content. | HTTP semantics | Sending a JSON body contradicts the status semantics. | live response body assertion |
| Creation returns `201` and identifies the created resource with `Location`. | course API policy | Consumers can follow the resource without reconstructing a URI. | provider-neutral scenario |
| Unsupported upload part media types return `415`. | course contract decision | Validation errors and unsupported formats require different remediation. | multipart negative test |
| All examples validate against the effective schema. | course publication policy | Examples are consumer input and generation seeds. | `make -C capstone examples` |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Operations, Parameters, and HTTP Messages claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Operations, Parameters, and HTTP Messages document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
/projects/{projectId}/datasets:
  parameters:
    - $ref: ../components/parameters/ProjectId.yaml
  get:
    operationId: listProjectDatasets
    parameters:
      - $ref: ../components/parameters/Limit.yaml
      - $ref: ../components/parameters/Cursor.yaml
      - name: status
        in: query
        required: false
        style: form
        explode: true
        schema:
          type: string
          enum: [awaiting-upload, ready]
    responses:
      '200':
        description: One page of datasets
        headers:
          X-Request-Id:
            $ref: ../components/headers/RequestId.yaml
        content:
          application/json:
            schema:
              $ref: ../components/schemas/DatasetPage.yaml
  post:
    operationId: createDataset
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: ../components/schemas/DatasetCreate.yaml
    responses:
      '201':
        description: Dataset registered
        headers:
          Location:
            $ref: ../components/headers/Location.yaml
        content:
          application/json:
            schema:
              $ref: ../components/schemas/Dataset.yaml
```

### Close reading

- Path-level `ProjectId` applies to both list and create operations; operation parameters add rather than replace it.
- `status` uses the default query `form` style; the literal wire examples are `?status=ready` and `?status=awaiting-upload`.
- `requestBody.required` requires content, while `DatasetCreate.required` determines required JSON properties.
- `201` documents both representation and `Location`; consumers may depend on either.
- `X-Request-Id` is response metadata and should not be smuggled into the response JSON model.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Optional path parameter
- Array serialization drift
- Body requiredness confusion
- JSON body on 204

Save a short decision record with these headings:

```text
Decision:
Alternatives rejected:
Normative basis:
Consumer impact:
Provider impact:
Negative case:
Evidence command:
Known tool limitation:
```

## Python implementation

### Boundary implementation

```python
@app.get("/projects/{projectId}/datasets", response_model=DatasetPage, operation_id="listProjectDatasets")
async def list_project_datasets(
    project_id: Annotated[str, Path(alias="projectId", pattern=r"^prj_[0-9]{4,18}$")],
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, pattern=r"^[0-9]+$"),
    status: Literal["awaiting-upload", "ready"] | None = Query(default=None),
    principal: Principal = Depends(require_scopes("datasets:read")),
) -> DatasetPage:
    items, next_cursor = store.list_datasets(project_id, principal.subject, principal.admin, limit, cursor, status)
    return DatasetPage(items=items, nextCursor=next_cursor)
```

### Why the code is shaped this way

- Path aliases keep the public camelCase identity while Python variables remain idiomatic.
- Query bounds are duplicated intentionally at runtime; the canonical contract remains authoritative and shared fixtures detect disagreement.
- FastAPI can coerce query strings to integers. Tests must show which strings are accepted rather than assuming Python type hints define the wire grammar.
- Problem translation must replace FastAPI’s default validation JSON with the public validation problem schema.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_cursor_and_invalid_limit_are_distinct(client, write_headers):
    for index in range(3):
        assert client.post("/projects", headers=write_headers, json={"name": f"P{index}"}).status_code == 201

    first = client.get("/projects?limit=2", headers=write_headers)
    assert first.status_code == 200
    assert len(first.json()["items"]) == 2
    assert first.json()["nextCursor"] is not None

    invalid = client.get("/projects?limit=0", headers=write_headers)
    assert invalid.status_code == 422
    assert invalid.headers["content-type"].startswith("application/problem+json")
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Operations, Parameters, and Messages check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
const listDatasetsRouteSchema = {
  querystring: Type.Object(
    {
      limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 50, default: 20 })),
      cursor: Type.Optional(Type.String({ pattern: "^[0-9]+$" })),
      status: Type.Optional(
        Type.Union([Type.Literal("awaiting-upload"), Type.Literal("ready")]),
      ),
    },
    { additionalProperties: false },
  ),
  response: {
    200: DatasetPageSchema,
    401: ProblemSchema,
    403: ProblemSchema,
    404: ProblemSchema,
    422: ValidationProblemSchema,
  },
} satisfies FastifySchema;
```

### Why the code is shaped this way

- `additionalProperties: false` rejects undocumented query keys instead of silently ignoring client mistakes.
- Fastify/Ajv coercion policy is explicit in app configuration. A query string is still text on the wire, so coercion behavior needs parity tests.
- The response schema closes the public page representation and prevents internal store fields from leaking.
- Use the same literal URI cases in Python, TypeScript, Prism, and live conformance.

### Focused test excerpt

```typescript
it("serializes a bounded cursor page and rejects limit zero", async () => {
  for (let index = 0; index < 3; index += 1) {
    await app.inject({ method: "POST", url: "/projects", headers: writeHeaders, payload: { name: `P${index}` } });
  }

  const first = await app.inject({ method: "GET", url: "/projects?limit=2", headers: writeHeaders });
  expect(first.statusCode).toBe(200);
  expect(first.json<{ items: unknown[]; nextCursor: string | null }>().items).toHaveLength(2);
  expect(first.json<{ nextCursor: string | null }>().nextCursor).not.toBeNull();

  const invalid = await app.inject({ method: "GET", url: "/projects?limit=0", headers: writeHeaders });
  expect(invalid.statusCode).toBe(422);
  expect(invalid.headers["content-type"]).toContain("application/problem+json");
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Operations, Parameters, and HTTP Messages, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Operations, Parameters, and HTTP Messages, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Optional path parameter | A template variable is marked optional or omitted. | Call the route without the segment and compare routing behavior. | Path parameters are always required; use a different path for a different target. |
| Array serialization drift | Contract expects repeated keys while a client sends comma-separated text. | Compare `?tag=a&tag=b` with `?tag=a,b`. | Set `style`/`explode`, publish a literal example, and test it. |
| Body requiredness confusion | Object properties are required but the entire request body is optional. | Send the operation with no content. | Set `requestBody.required: true` separately. |
| JSON body on 204 | Handler returns an empty object with `204`. | Inspect raw content length and bytes. | Return no content or choose a status that permits a representation. |
| Wrong problem media type | A 422 body uses `application/json` while contract says Problem Details. | Assert `Content-Type` on a malformed request. | Translate framework errors at one boundary. |
| Missing Location | A 201 response returns the new object but no URI. | Inspect response fields after creation. | Emit and document `Location` from canonical resource identity. |
| Unknown query silently ignored | Typos produce broad results instead of rejection. | Call `?stats=ready`. | Close query objects or explicitly document tolerance policy. |

### Defect-injection protocol

Use the module lab to inject the named operations, parameters, and messages defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Complete project and dataset operations with exact parameter locations, serialization, request bodies, response fields, status codes, and media types.

This Operations, Parameters, and HTTP Messages increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/paths/projects.yaml`
- `capstone/spec/paths/project.yaml`
- `capstone/spec/paths/project-datasets.yaml`
- `capstone/spec/paths/dataset.yaml`
- `capstone/spec/components/parameters/`
- `capstone/spec/components/headers/`
- `capstone/services/python-fastapi/src/analysis_api/app.py`
- `capstone/services/typescript-fastify/src/app.ts`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- project/dataset message surface
- parameter serialization matrix
- status/media-type negative cases
- cross-provider request collection

### Commit boundary

The Operations, Parameters, and HTTP Messages checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Model path, query, header, cookie, and body input deliberately, Use request bodies and media types correctly, and Describe response codes, headers, and representations as a complete outcome** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a body on one 204 response, demonstrate the failing raw-byte assertion, then repair it** and requiring the following oracle: **every value has one intentional wire location; serialization has literal examples; 201 includes Location; 204 carries no content.**

The cumulative platform now includes **Complete project and dataset messages, including pagination inputs, creation responses, and problem representations**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [JSON Schema Contract Modeling](../module-03-json-schema-contract-modeling/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
