# Module 10 — OpenAPI 3.2, Streaming, Webhooks, and Workflows

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How do current OpenAPI features express streaming, webhooks, links, query methods, and multi-step workflows?

## Where this module fits

Module 09 produced **Create compatible and rejected release candidates, compatibility gates, and public/partner audience views**. This final module consolidates the course by asking: **How do current OpenAPI features express streaming, webhooks, links, query methods, and multi-step workflows?**

The capstone must now deliver **Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow** while preserving every earlier module result. Successful completion establishes the outgoing boundary for the next course or final program defense: **A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflow description, compatibility policy, and provider-neutral behavioral scenarios.**

## Learning outcomes

- Maintain a broadly executable OpenAPI 3.1 baseline.
- Use OpenAPI 3.2 features where they add real meaning.
- Model SSE and JSON Lines streams.
- Connect operations with links, callbacks, webhooks, and runtime expressions.
- Describe a multi-step outcome with Arazzo and record tool support honestly.

## Capstone increment

Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow.

## Core model

### Driving question

> How do we adopt current advanced capabilities without overstating what today’s tools execute?

### Observable outcome

Upgrade a maintained frontier contract to OpenAPI 3.2.0, model hierarchy, QUERY, complete query strings, sequential media, callbacks/webhooks/links, and an Arazzo 1.1 workflow, then publish an executed tool-capability report.

### 1. A baseline and a frontier solve different release problems

The executable baseline uses OpenAPI 3.1.2 because the selected generators and framework integrations have broad 3.1 support. The frontier description upgrades the same API to 3.2.0 and exercises current constructs. The two artifacts share operation identity and domain semantics; the frontier is not a speculative rewrite.

This dual-track design avoids two dishonest extremes: freezing the course on an old specification or claiming that every tool fully implements the newest one. Promotion from frontier to baseline requires measured support across publication, generation, testing, and runtime adapters.
### 2. OpenAPI 3.2 remains compatible with 3.1 descriptions

A valid 3.1 description is intended to remain valid under 3.2, while new 3.2 fields require 3.2-aware tooling. Upgrade begins by changing the version and running a 3.2-aware validator before adopting new syntax. Existing semantics are preserved unless the author deliberately changes them.

The capstone maintains separate bundles and compares their common operation set. A tool that parses the frontier while silently dropping a new field is classified as partial, not fully supported.
### 3. Enhanced tags provide native document hierarchy

OpenAPI 3.2 Tag Objects can carry a short `summary`, a `parent` relationship, and a `kind` classification. This supports navigable domain groupings without proprietary display extensions. Parent references must point to existing tag names and must not form cycles.

The frontier groups Projects, Datasets, Runs, Artifacts, and Webhooks under domain parents while keeping operation tags stable. Rendering quality is observed separately from structural validation because tools may parse the fields without displaying them.
### 4. Additional operations model methods outside the fixed Path Item fields

OpenAPI 3.2 introduces `additionalOperations` so a Path Item can describe methods beyond `get`, `post`, and the traditional fixed set. The frontier uses HTTP `QUERY` for an analysis search experiment. This is a standards exercise, not a claim that browsers, proxies, frameworks, or generators uniformly support the method.

The API retains a conventional `POST /analysis-searches` fallback in 3.1-compatible deployments. Capability evidence distinguishes schema acceptance, server routing, client generation, mock support, and intermediary viability.
### 5. The querystring parameter describes the complete query component

A 3.2 Parameter Object with `in: querystring` models the entire query string as one value rather than independent named parameters. This can describe structured query languages or signatures where order and whole-string grammar matter. It is not a replacement for ordinary named query parameters.

The frontier QUERY experiment uses a complete query-string schema and examples. Tests retain the raw target rather than allowing a framework parser to normalize away significant syntax.
### 6. Sequential media needs item semantics

Streaming formats such as server-sent events, JSON Lines, and JSON text sequences carry a sequence of logical items rather than one JSON document. OpenAPI 3.2’s Media Type Object can describe individual items with `itemSchema`. The enclosing media type and framing rules still matter.

The capstone documents SSE and NDJSON progress. `itemSchema` describes each progress event, while prose and examples define `data:` framing or newline separation. A validator that only checks the whole byte stream as JSON is the wrong proof tool.
### 7. Callbacks, webhooks, and links answer different questions

A callback is an operation the provider may invoke at a URL derived from the initiating request. A root-level webhook describes an inbound event operation that may occur independently of one specific operation declaration. A Link Object describes how response data supplies parameters for another API operation; it does not send a request.

The contract uses a callback example for per-run notification, a root webhook for completion-event shape, and links from accepted/completed runs to status and artifacts. Choosing one based on visual similarity produces incorrect workflows.
### 8. Runtime expressions connect messages

Runtime expressions can extract values from request URLs, parameters, bodies, response headers, and response bodies. They are used in callback keys and Link parameters. The expression is evaluated against a concrete exchange, so the selected value must exist in every response branch where the link appears.

The lab checks expressions against fixtures: run ID from `$response.body#/id`, status URI from a response field, and callback destination from request content. A syntactically valid expression pointing to an optional absent property is a workflow defect.
### 9. Arazzo describes an outcome-oriented sequence

An Arazzo document references source descriptions, declares workflows, accepts inputs, executes operation steps, captures outputs, and expresses dependencies or success criteria. It is not an orchestration engine, test framework, or replacement for the OpenAPI contract.

The capstone workflow creates a project, registers and uploads a dataset, starts analysis, inspects status, and retrieves artifacts. Polling and asynchronous waiting are represented within the limits of the runner; unsupported waiting or webhook reception is called out rather than simulated as success.
### 10. Capability reporting is part of advanced engineering

“Supports OpenAPI 3.2” can mean parses the version string, validates new fields, renders them, generates clients, mocks behavior, or tests a live provider. The report probes each material feature and stage separately with exact tool versions and commands.

Results use supported, partial, transformed, unsupported, or not executed. A failed installation is not evidence of unsupported semantics; it is reported as not executed. This distinction is essential when course artifacts are reviewed outside the author’s environment.
### 11. Graceful degradation must preserve contract intent

When a 3.1-only consumer cannot process enhanced tags, the loss is presentational. When it cannot represent QUERY or `itemSchema`, functionality or validation may be lost. Fallbacks therefore depend on semantic importance: ignore safe metadata, transform to an equivalent operation, maintain a 3.1 view, or block use.

The frontier-to-baseline map names each transformation. No script simply deletes unknown keys and labels the result equivalent.

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

1. Why keep 3.1.2 and 3.2.0 artifacts?
2. What must “supports 3.2” specify?
3. When is `in: querystring` appropriate?
4. What does `itemSchema` not describe?
5. Distinguish callback, webhook, and link.

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For OpenAPI 3.2, Streaming, and Arazzo Workflows, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| The maintained executable baseline remains OpenAPI 3.1.2 until the required toolchain passes promotion criteria. | release strategy | Current tool support is uneven across validation, generation, rendering, and testing. | capability matrix |
| The frontier description uses OpenAPI 3.2.0 and preserves common operation identities. | course currency rule | Learners must understand the current specification without splitting the domain. | frontier parse and operation comparison |
| New 3.2 constructs are validated by a 3.2-aware route and probed per tool capability. | evidence policy | Parsing an old subset is not proof of new-field support. | capability report |
| Callbacks, webhooks, and links are selected by invocation semantics, not interchangeable syntax. | modeling rule | They describe different directions and triggers. | workflow fixture checks |
| Arazzo steps reference real operationIds and their inputs/outputs resolve against source operations. | workflow integrity rule | A readable workflow with broken references is not executable evidence. | workflow validator |
| Not-executed tool probes are reported distinctly from unsupported features. | honesty rule | Environment failure does not establish semantic incapability. | tool capability report |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every OpenAPI 3.2, Streaming, and Arazzo Workflows claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the OpenAPI 3.2, Streaming, and Arazzo Workflows document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
openapi: 3.2.0

tags:
  - name: Analysis domain
    summary: Submit and observe analysis work
    kind: nav
  - name: Runs
    summary: Analysis-run lifecycle operations
    parent: Analysis domain
    kind: nav

paths:
  /analysis-query:
    additionalOperations:
      QUERY:
        operationId: queryAnalysisRuns
        tags: [Runs]
        parameters:
          - name: expression
            in: querystring
            required: true
            schema:
              type: string
              minLength: 1
        responses:
          '200':
            description: Matching analysis runs
            content:
              application/json:
                schema:
                  $ref: ./components/schemas/AnalysisRunPage.yaml

  /analysis-runs/{runId}/events:
    get:
      operationId: streamAnalysisRunEvents
      responses:
        '200':
          description: Sequential progress events
          content:
            application/x-ndjson:
              itemSchema:
                $ref: ./components/schemas/ProgressEvent.yaml
```

### Close reading

- `additionalOperations` carries the non-fixed QUERY method while retaining an ordinary Path Item.
- `in: querystring` describes the complete query component and its name is descriptive rather than a conventional key lookup.
- `itemSchema` describes each sequential item; the NDJSON framing remains a media-format concern.
- Enhanced tag parent names must resolve and form an acyclic hierarchy.
- The 3.1 baseline offers conventional operations for capabilities that older tools cannot represent.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Version bump only
- Parser acceptance called full support
- Complete query normalized as parameters
- Stream validated as one JSON document

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
async def ndjson_events(run_id: str, principal: Principal) -> StreamingResponse:
    run = store.get_owned_run(principal.subject, run_id)

    async def generate():
        for event in store.progress_events(run.id):
            payload = ProgressEvent.model_validate(event).model_dump(mode="json")
            yield json.dumps(payload, separators=(",", ":")) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")
```

### Why the code is shaped this way

- Each event is validated independently before framing; the stream as a whole is not one JSON document.
- Production streaming must address disconnects, backpressure, heartbeats, authorization lifetime, and bounded buffers.
- FastAPI’s generated 3.1 description may need manual canonical documentation for 3.2 `itemSchema`.
- The capability report records runtime support separately from OpenAPI generation support.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_ndjson_stream_contains_schema_valid_items(client, write_headers):
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    accepted = client.post(
        "/analysis-runs",
        headers={**write_headers, "Idempotency-Key": "stream-0001"},
        json={
            "projectId": project_id,
            "datasetId": dataset_id,
            "parameters": {"algorithm": "line-count"},
        },
    )
    response = client.get(
        f"/analysis-runs/{accepted.json()['id']}/events",
        headers={**write_headers, "Accept": "application/x-ndjson"},
    )

    events = [json.loads(line) for line in response.text.splitlines() if line]
    assert response.status_code == 200
    assert events[-1]["status"] == "completed"
    assert all({"eventId", "runId", "status", "progress", "occurredAt"} <= event.keys() for event in events)
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused OpenAPI 3.2, Streaming, Webhooks, and Workflows check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
import { Value } from "@sinclair/typebox/value";

app.get("/analysis-runs/:runId/events", {
  preHandler: requireScopes(["runs:read"]),
}, async (request, reply) => {
  const run = store.getOwnedRun(request.principal.subject, request.params.runId);
  const events = store.progressEvents(run.id);
  for (const event of events) {
    if (!Value.Check(ProgressEventSchema, event)) {
      throw new Error("stored progress event violates the public schema");
    }
  }

  reply.raw.setHeader("content-type", "application/x-ndjson");
  for (const event of events) {
    reply.raw.write(`${JSON.stringify(event)}\n`);
  }
  reply.raw.end();
  return reply;
});
```

### Why the code is shaped this way

- Use a real runtime schema validator for each event; a TypeScript annotation alone does not validate stored data.
- Direct raw response writing bypasses some Fastify serialization behavior, so headers and error-before-stream rules need focused tests.
- Once bytes are sent, a later error cannot become a normal Problem Details response; validate prerequisites first.
- QUERY routing support is probed separately and the 3.1 POST fallback remains the deployable baseline.

### Focused test excerpt

```typescript
it("emits independently parseable NDJSON progress items", async () => {
  const { projectId, datasetId } = await createReadyDataset(app);
  const accepted = await app.inject({
    method: "POST",
    url: "/analysis-runs",
    headers: { ...writeHeaders, "idempotency-key": "stream-0001" },
    payload: { projectId, datasetId, parameters: { algorithm: "line-count" } },
  });
  const stream = await app.inject({
    method: "GET",
    url: `/analysis-runs/${accepted.json<{ id: string }>().id}/events`,
    headers: { ...writeHeaders, accept: "application/x-ndjson" },
  });

  const events = stream.body.split("\n").filter(Boolean).map((line) => JSON.parse(line));
  expect(stream.statusCode).toBe(200);
  expect(events.at(-1)).toMatchObject({ status: "completed", progress: 100 });
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For OpenAPI 3.2, Streaming, and Arazzo Workflows, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For OpenAPI 3.2, Streaming, and Arazzo Workflows, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Version bump only | Document says 3.2 but no new feature is understood or tested. | Insert malformed enhanced tag or QUERY structure. | Use a 3.2-aware validator and feature probes. |
| Parser acceptance called full support | Tool ignores parent/itemSchema while returning success. | Inspect rendered/generated/tested behavior. | Score capability per stage and feature. |
| Complete query normalized as parameters | Order or grammar is destroyed by framework parsing. | Send encoded/reordered raw query cases. | Preserve raw query target or use conventional fallback. |
| Stream validated as one JSON document | NDJSON/SSE fails a normal JSON parser. | Feed multiple framed events. | Validate itemSchema per item plus framing-specific tests. |
| Callback confused with webhook | Direction/trigger is documented incorrectly. | Ask where URL originates and which event initiates call. | Use callback for request-derived destination; root webhook for independent inbound event. |
| Link treated as invocation | Docs imply provider calls linked operation. | Observe no outbound request. | Describe link as consumer navigation/parameter relation. |
| Broken runtime expression | Link points to optional or wrong response path. | Evaluate against every named response fixture. | Use stable required source value or conditionally place link. |
| Arazzo as fake automation | Unsupported wait/webhook step is marked passed. | Run workflow runner and inspect boundary. | State unsupported orchestration explicitly and separate manual evidence. |
| Unknown fields stripped for fallback | 3.2 functionality disappears silently. | Compare operation and feature maps after conversion. | Use deliberate transformation with semantic inventory. |

### Defect-injection protocol

Use the module lab to inject the named openapi 3.2, streaming, webhooks, and workflows defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Upgrade a maintained frontier contract to OpenAPI 3.2.0, model hierarchy, QUERY, complete query strings, sequential media, callbacks/webhooks/links, and an Arazzo 1.1 workflow, then publish an executed tool-capability report.

This OpenAPI 3.2, Streaming, and Arazzo Workflows increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/openapi-3.2.yaml`
- `capstone/spec/paths/analysis-query-3.2.yaml`
- `capstone/spec/paths/analysis-run-events-3.2.yaml`
- `capstone/spec/workflows/analysis-run.arazzo.yaml`
- `capstone/spec/components/schemas/ProgressEvent.yaml`
- `capstone/reports/tool-capability.json`
- `capstone/docs/tooling-boundaries.md`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- OpenAPI 3.2 frontier
- stream/QUERY feature probes
- validated callback/webhook/link expressions
- Arazzo workflow and capability report

### Commit boundary

The OpenAPI 3.2, Streaming, and Arazzo Workflows checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Course exit

The ten module results now satisfy this course promise: A modular OpenAPI 3.1 contract, a current OpenAPI 3.2 frontier, conforming Python and TypeScript providers, usable clients, and controlled release evidence. The next course is **Contract-Driven API Service Engineering**; it consumes the outgoing handoff rather than reinterpreting completed work.

## Module synthesis

You are ready to leave this module when you can **Maintain a broadly executable OpenAPI 3.1 baseline, Use OpenAPI 3.2 features where they add real meaning, and Model SSE and JSON Lines streams** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **3.2 frontier validates independently; common operation identities remain stable; tag hierarchy resolves without cycles; QUERY/querystring and sequential itemSchema are present.**

The cumulative platform now includes **Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Complete the course final defense and outgoing handoff described in [Capstone](../capstone.md). Course 2 may treat only the manifested handoff as settled.
