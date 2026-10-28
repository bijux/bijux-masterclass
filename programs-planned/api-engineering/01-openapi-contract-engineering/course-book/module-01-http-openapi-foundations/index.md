# Module 01 — HTTP and OpenAPI Foundations

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?

## Where this module fits

Course 1 begins from this incoming boundary: **Basic programming ability, command-line familiarity, and no assumed OpenAPI experience.**

This module establishes the course’s first new responsibility by asking: **How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?** Its capstone increment is **Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior**. That result is required before **Operations, Parameters, and Messages** can be studied honestly.

## Learning outcomes

- Read requests and responses as protocol messages.
- Separate API behavior, OpenAPI description, implementation, and documentation rendering.
- Choose methods and status codes from HTTP semantics.
- Write a minimal valid OpenAPI description.
- Prove that the two reference providers expose the same public behavior.

## Capstone increment

Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior.

## Core model

### Driving question

> What behavior is the contract actually describing?

### Observable outcome

Describe and implement `GET /health`, `GET /projects`, `POST /projects`, and `GET /projects/{projectId}` without confusing HTTP semantics, OpenAPI structure, and framework behavior.

### 1. The wire message is the ground truth of an interaction

An HTTP request is not “a function call over the network.” It has a method, a target URI, field lines, and possibly content. The response has a status, fields, and possibly content. OpenAPI describes admissible messages at this boundary. It does not describe Python stack frames, TypeScript objects, database rows, or controller names.

Begin every operation by writing one raw exchange. For project creation, the observable contract includes `POST /projects`, `Content-Type: application/json`, a JSON representation, `201 Created`, a `Location` field, and a response media type. If any of those differ at runtime, the provider has drifted even when its internal function returned a correct object.
### 2. Resource, representation, and endpoint are different ideas

A project is the conceptual resource. `/projects/prj_0001` is one identifier for it. The JSON document returned today is a representation of its current state. An OpenAPI Path Item groups operations addressable through one path template; it is not the resource itself.

This distinction prevents designs such as `/getProjectObject` or `/callCreateProject`. Paths should remain stable when handler classes, frameworks, and storage models change. Representations may evolve under compatibility rules, while resource identity and operation identity require deliberate migration.
### 3. Method semantics constrain clients and intermediaries

`GET` is defined as safe: the client does not request a state change. `PUT`, `DELETE`, and safe methods are idempotent in their intended effect; `POST` is not automatically idempotent. These properties affect retry behavior, caches, prefetchers, and generated client expectations.

A read handler incrementing an internal metric does not make `GET` unsafe, because incidental server-side effects are permitted. A `GET /projects/{id}/delete` operation is unsafe because deletion is the requested effect. Naming cannot repair the wrong method.
### 4. The OpenAPI document is an object graph

The root OpenAPI Object declares the specification version, metadata, servers, paths, reusable components, and security defaults. A path key leads to a Path Item Object; a method field leads to an Operation Object; an operation leads to parameters, request content, responses, callbacks, links, and security requirements.

Indentation is therefore semantic in YAML. Moving `responses` one level can turn an operation response map into an unknown Path Item field. A renderer may recover or omit the mistake; a parser and structural validator must reject it.
### 5. `operationId` is consumer-facing identity

Many generators turn `operationId: createProject` into a method named `create_project` or `createProject`. Renaming it while leaving `POST /projects` unchanged can break consumers. The capstone requires global uniqueness and tests provider handler maps against the canonical operation ledger.

Use names that describe stable outcomes rather than implementation: `getProject`, not `projectControllerV2`. Treat a rename as a compatibility change, not a refactor hidden inside YAML.
### 6. A valid description is not a conforming runtime

A specification can parse while the provider returns `200` instead of `201`, emits `text/plain`, accepts undocumented input, or leaks an internal field. Conversely, a working provider may have no complete contract. Static checks prove document properties; live checks prove observed behavior.

The course keeps four evidence layers separate: source validation, provider unit tests, provider-neutral live conformance, and consumer execution. A green documentation page belongs to none of those proof categories.

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

1. Write the complete raw request and response for creating a project named `Atlas`. Include the minimum fields that establish the contract.
2. Classify each method as safe and/or idempotent: GET, POST, PUT, DELETE.
3. Explain why an internal analytics counter does not make a GET operation unsafe.
4. Find the structural error when `responses` is aligned with `get` rather than nested under it.
5. Why can changing only `operationId` be breaking?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For HTTP and OpenAPI Foundations, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Every Operation Object has a non-empty `responses` map. | OAS requirement | An operation without any described response is incomplete. | `make -C capstone parse` |
| A templated path variable has a matching path parameter whose `required` value is `true`. | OAS requirement | The legal request target cannot be derived otherwise. | reference and structural gates |
| `GET` is safe and `POST` is not inherently idempotent. | HTTP semantics | Retries and automated retrieval depend on the method contract. | raw-message exercises and live behavior |
| Success response media types are explicitly described. | course policy | Implicit JSON assumptions produce generator and negotiation drift. | example validation and live content-type assertions |
| Every path operation has one globally unique stable `operationId`. | course compatibility policy | Generated consumer method names depend on it. | operation ledger and handler-map gate |
| The hand-authored multi-document description is canonical. | architecture decision | Framework output differs and is used as drift evidence. | provider comparison in Module 06 |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every HTTP and OpenAPI Foundations claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the HTTP and OpenAPI Foundations document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
openapi: 3.1.2
info:
  title: Analysis Runs API
  version: 1.0.0
servers:
  - url: http://127.0.0.1:8000
paths:
  /health:
    get:
      operationId: getHealth
      summary: Check service health
      security: []
      responses:
        '200':
          description: Service is accepting requests
          content:
            application/json:
              schema:
                $ref: ./components/schemas/Health.yaml
  /projects/{projectId}:
    parameters:
      - $ref: ./components/parameters/ProjectId.yaml
    get:
      operationId: getProject
      summary: Retrieve a project
      responses:
        '200':
          description: Project representation
          content:
            application/json:
              schema:
                $ref: ./components/schemas/Project.yaml
        '404':
          $ref: ./components/responses/NotFound.yaml
```

### Close reading

- `security: []` is an explicit anonymous override for health; absence would inherit global security later.
- The path-level parameter applies to every operation under the Path Item and must match `{projectId}` exactly.
- Quoted response codes remain strings in YAML and avoid accidental numeric-key behavior across parsers.
- The schema reference is resolved relative to the file containing the reference, not the shell working directory.
- The fragment says nothing about whether the provider truly returns the status, fields, or media type; live evidence is still required.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- State-changing GET
- Creation returns generic 200
- Path variable is undocumented
- Duplicate operation identity

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
@app.get(
    "/health",
    response_model=Health,
    operation_id="getHealth",
    tags=["System"],
)
async def get_health() -> Health:
    return Health(
        status="ok",
        service="analysis-runs-api",
        version="1.0.0",
        time=utcnow(),
    )

@app.post(
    "/projects",
    response_model=Project,
    status_code=201,
    operation_id="createProject",
    tags=["Projects"],
)
async def create_project(body: ProjectCreate, response: Response, principal=Depends(...)) -> Project:
    project = store.create_project(principal.subject, body)
    response.headers["Location"] = f"/projects/{project.id}"
    response.headers["ETag"] = store.etag(project)
    return project
```

### Why the code is shaped this way

- `response_model` is both validation and serialization allowlist; it must match the canonical response schema rather than an internal model.
- FastAPI’s generated OpenAPI is intentionally not used as the source of truth. The explicit `operation_id` permits mechanical handler mapping.
- Creation status and headers are set at the adapter boundary because they are HTTP behavior, not store behavior.
- Add tests that inspect status, `Content-Type`, `Location`, `ETag`, and response shape—not only returned Python values.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_create_project_wire_contract(client, write_headers):
    response = client.post("/projects", headers=write_headers, json={"name": "Boundary lab"})

    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")
    assert response.headers["location"] == f"/projects/{response.json()['id']}"
    assert response.headers["etag"] == '"prj_0001:1"'
    assert set(response.json()) == {
        "id", "ownerId", "name", "description", "version", "createdAt", "updatedAt"
    }
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused HTTP and OpenAPI Foundations check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
app.post(
  "/projects",
  {
    preHandler: requireScopes("projects:write"),
    schema: {
      operationId: "createProject",
      tags: ["Projects"],
      body: ProjectCreateSchema,
      response: { 201: ProjectSchema, 401: ProblemSchema, 403: ProblemSchema, 422: ValidationProblemSchema },
    },
  },
  async (request, reply) => {
    const project = store.createProject(principal(request), request.body as ProjectCreate);
    return reply
      .code(201)
      .header("Location", `/projects/${project.id}`)
      .header("ETag", store.etag(project))
      .send(project);
  },
);
```

### Why the code is shaped this way

- Fastify uses route schemas for runtime validation and response serialization; TypeScript types alone disappear at runtime.
- The schema lists public responses so Fastify cannot silently serialize a different success representation.
- `as ProjectCreate` only helps the compiler after runtime validation. It is not a substitute for `ProjectCreateSchema`.
- The shared live suite must see the same message as the Python provider despite different framework internals.

### Focused test excerpt

```typescript
it("creates the documented project representation", async () => {
  const response = await app.inject({
    method: "POST",
    url: "/projects",
    headers: writeHeaders,
    payload: { name: "Boundary lab" },
  });

  expect(response.statusCode).toBe(201);
  expect(response.headers.location).toBe(`/projects/${response.json<{ id: string }>().id}`);
  expect(response.headers.etag).toBe('"prj_0001:1"');
  expect(response.headers["content-type"]).toContain("application/json");
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For HTTP and OpenAPI Foundations, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For HTTP and OpenAPI Foundations, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| State-changing GET | `GET /projects/{id}/delete` appears convenient but requests deletion. | Send the GET twice and observe resource disappearance. | Choose `DELETE` or a command resource and test retry semantics. |
| Creation returns generic 200 | Framework default is accepted without reviewing HTTP outcome. | Assert `201` and `Location` after `POST /projects`. | Set status and fields explicitly in both contract and adapter. |
| Path variable is undocumented | `/projects/{projectId}` exists but no required path parameter does. | Bundle and inspect the operation parameter set. | Declare one required `in: path` parameter with the exact name. |
| Duplicate operation identity | Two handlers use `getProject`. | Generate the operation ledger or a client. | Use globally unique stable IDs and gate them. |
| YAML boolean surprise | Unquoted values such as older YAML `on`/`off` forms change type in some parsers. | Parse YAML and inspect scalar types rather than the rendered page. | Use a YAML 1.2-aware toolchain and quote ambiguous scalars. |
| Renderer-as-proof | Swagger UI displays an operation, so the implementation is assumed conformant. | Return an undocumented status from the provider. | Run live status, header, media-type, and schema assertions. |

### Defect-injection protocol

Use the module lab to inject the named http and openapi foundations defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Describe and implement `GET /health`, `GET /projects`, `POST /projects`, and `GET /projects/{projectId}` without confusing HTTP semantics, OpenAPI structure, and framework behavior.

This HTTP and OpenAPI Foundations increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/openapi.yaml`
- `capstone/spec/paths/health.yaml`
- `capstone/spec/paths/projects.yaml`
- `capstone/spec/components/schemas/Health.yaml`
- `capstone/spec/components/schemas/Project.yaml`
- `capstone/services/python-fastapi/src/analysis_api/app.py`
- `capstone/services/typescript-fastify/src/app.ts`
- `capstone/tests/conformance/behavioral-scenarios.yaml`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- four-operation canonical slice
- raw HTTP exchange notebook
- two provider smoke tests
- first operation ledger

### Commit boundary

The HTTP and OpenAPI Foundations checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Read requests and responses as protocol messages, Separate API behavior, OpenAPI description, implementation, and documentation rendering, and Choose methods and status codes from HTTP semantics** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Temporarily change one provider to return 200 for project creation** and requiring the following oracle: **four introductory operations have unique stable IDs; project creation is 201 with Location and JSON; the path parameter is explicitly required; health is explicitly anonymous.**

The cumulative platform now includes **Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Operations, Parameters, and Messages](../module-02-operations-parameters-messages/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
