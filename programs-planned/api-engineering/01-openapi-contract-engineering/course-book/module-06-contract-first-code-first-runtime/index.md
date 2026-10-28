# Module 06 — Contract-First and Code-First Runtimes

> **Program stage:** Course 1 of 6 — Specify the promise.

> **Central question:** How do design-first and code-first descriptions relate, and how is semantic drift detected?

## Where this module fits

Map every operation to a handler and compare canonical, generated, and observed descriptions. You arrive from Module 05 with all earlier checkpoints still green. This course owns the public contract. It can describe downstream consequences, but it does not claim that persistence, authorization, or operations are correct merely because the document is valid. The result is the baseline for **Mocks, Clients, and Contract Testing**.

## Learning outcomes

- Keep the canonical contract authoritative.
- Translate framework validation errors into the public problem model.
- Validate responses as well as requests.
- Classify generated-description drift.
- Preserve equivalent observable behavior across FastAPI and Fastify.

## Capstone result

Map every operation to both providers and compare generated observations with the canonical contract.

Both providers implement the complete contract and pass one provider-neutral behavioral suite.

## Core model

### Driving question

> How do we prove that two different frameworks implement one public contract?

### Observable outcome

Finish the FastAPI and Fastify providers, compare framework-generated observations to the canonical description, translate framework defaults, and pass one provider-neutral behavioral suite.

### 1. Source of truth is an architectural decision

A design-first system begins with a reviewed contract and asks providers and consumers to conform. A code-first system derives a description from runtime declarations. A schema-first system may begin with shared data schemas but still needs explicit HTTP decisions. None is universally correct, but mixing them without naming authority guarantees drift.

The capstone uses a hand-authored, multi-document contract as the normative source. FastAPI and Fastify can each emit an OpenAPI document, but those documents are observations of framework configuration. They are compared to the canonical contract; they do not overwrite it. This preserves language neutrality and prevents one provider's defaults from becoming accidental public policy.
### 2. Framework-generated descriptions are useful evidence

Generated descriptions expose what a framework believes it serves: inferred response codes, validation statuses, nullable shapes, route parameters, and security declarations. That makes them valuable drift sensors. They are weak as the sole truth when the API spans multiple implementations or uses features outside the framework's model.

Normalize before comparison. Ignore ordering, generated server URLs, and harmless documentation text only when an allowlist names the exact path and reason. Never normalize away a changed status, parameter location, required property, media type, or security requirement.
### 3. Request validation and response serialization solve different problems

Request validation rejects messages outside the admitted input set. Response serialization restricts what the provider releases and confirms that output satisfies the public representation. A service can validate input rigorously while leaking internal ownership, idempotency fingerprints, or database fields in its response.

Both capstone providers therefore define input models and output schemas separately. The tests send extra input fields, force internal values into stored objects, and verify that undeclared output fields never cross the boundary. Static TypeScript types do not perform either runtime function by themselves.
### 4. Framework errors are not public contracts

FastAPI and Fastify have different default validation shapes, status choices, field paths, and wording. Exposing either default makes consumers framework-dependent and destroys provider parity. The adapter must translate native failures into the canonical `application/problem+json` representation.

Translation keeps machine identity stable: problem `type`, HTTP `status`, title category, and a documented `errors` extension. Internal exception classes, stack traces, schema-library wording, and framework URLs remain private. The same invalid request must be externally equivalent even when diagnostic internals differ.
### 5. Handler traceability closes the implementation gap

A parsed contract can contain an operation no provider implements. A provider can expose an undocumented route. The operation ledger extracts method, path, and `operationId` from the canonical bundle; language-specific maps extract the same identity from route declarations. The checkpoint compares both sets in both directions.

Traceability is stronger than counting routes. It detects a handler attached to the wrong method, a renamed `operationId`, a canonical operation omitted by one provider, and an extra internal route unintentionally made public. Internal framework routes such as documentation endpoints must be explicitly excluded or disabled.
### 6. Parity means equivalent public behavior, not identical internals

FastAPI uses Pydantic models and dependency injection. Fastify uses JSON Schema, hooks, and route options. Forcing identical class layout would be cargo-cult portability. The parity boundary is observable HTTP behavior: admitted requests, status, media type, stable headers, representation semantics, authorization outcomes, and lifecycle transitions.

Some nondeterminism must be normalized carefully. Identifiers and timestamps can differ across fresh runs, but their formats and relationships must match. A shared scenario should capture an identifier from one response and use it later rather than compare hard-coded values across providers.
### 7. A scenario is a stateful black-box specification

A useful scenario says more than “GET returns 200.” It creates prerequisites, sends a request, asserts status and media type, validates selected fields, captures outputs, and applies them to later steps. The Analysis Runs workflow creates a project, registers a dataset, uploads content, submits a run, observes progression, and retrieves artifacts.

Scenarios should remain provider-neutral. They receive a base URL and credentials, not an imported application object. Provider unit tests can be faster and more diagnostic, but only a black-box suite proves that deployment adapters expose the same boundary.
### 8. Coercion is public behavior

Frameworks often coerce query strings, path values, booleans, and numbers differently. One may accept `limit=01`, `limit=3.0`, or repeated scalar parameters while another rejects them. Unless the contract explicitly admits both representations, that difference is semantic drift.

The shared suite includes boundary and malformed serialization cases. Providers either configure matching coercion or reject ambiguous forms consistently. “The framework does that” is not an interoperability argument.
### 9. Drift allowlists need exact scope and expiry

Some generated differences are inevitable: title wording, schema component names, generated documentation routes, or order. An allowlist can suppress these only by exact JSON Pointer or comparison category, with rationale and owner. A wildcard over `responses` or `schemas` is equivalent to disabling the gate.

Each allowlisted item should be reviewed when framework versions change. The capstone keeps an intentionally small observation report rather than claiming semantic equality from a textual diff of two very different generated documents.
### 10. Contract tests complement, not replace, provider tests

Provider unit tests inspect domain invariants and precise failure branches. Contract tests inspect boundary conformance. Generated property tests search an input space. Consumer workflow tests validate usability. None subsumes all others.

The proof ladder runs cheap structural checks first, then focused provider suites, then live conformance, then generated and consumer tests. This ordering shortens diagnosis while preserving independent evidence.

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

1. When is code-first a defensible choice?
2. Why not require text-identical generated documents?
3. Name four semantic differences that may never be broadly allowlisted.
4. What does response serialization prove that request validation does not?
5. Why is an imported TestClient insufficient as the only parity proof?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Contract-First and Code-First Runtimes, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| The modular hand-authored OpenAPI description is canonical. | architecture decision | A language-neutral contract must not inherit one framework’s defaults. | canonical bundle and ADR 0001 |
| Every canonical path operation maps to exactly one public handler in each provider. | course completion rule | Missing and undocumented behavior must be mechanically visible. | `make -C capstone handler-map` |
| Framework validation failures are translated to the documented Problem representation. | public API policy | Consumers must not depend on FastAPI or Fastify internals. | negative provider and live tests |
| Response serialization admits only declared public properties. | security and conformance rule | Internal fields are implementation details and possible data leaks. | response schema tests |
| A drift allowlist cannot suppress method, path, parameter, media type, response, schema-requiredness, or security differences. | compatibility policy | Those differences change consumer behavior. | drift review exercise |
| Provider parity is evaluated through the same black-box scenarios. | evidence rule | Separate test suites can accidentally encode separate contracts. | live conformance report |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Contract-First and Code-First Runtimes claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Contract-First and Code-First Runtimes document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
paths:
  /analysis-runs:
    post:
      operationId: createAnalysisRun
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: ./components/schemas/AnalysisRunCreate.yaml
      responses:
        '202':
          $ref: ./components/responses/AnalysisRunAccepted.yaml
        '409':
          $ref: ./components/responses/Conflict.yaml
        '422':
          $ref: ./components/responses/ValidationFailed.yaml

components:
  responses:
    ValidationFailed:
      description: The request is structurally invalid
      content:
        application/problem+json:
          schema:
            $ref: ./schemas/ValidationProblem.yaml
```

### Close reading

- The operation identity is copied exactly into both route declarations and checked against the ledger.
- `422` describes the course’s public validation contract; native framework error payloads are translated before release.
- The accepted response is reusable only because all referenced operations share the same observable status, headers, and representation.
- The canonical contract does not encode Pydantic model names, TypeBox constructors, dependency functions, or route plugin structure.
- A generated framework description may name components differently; comparison focuses on semantic surface rather than text identity.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Generated document promoted to canonical
- Native validation payload leaked
- Response schema omitted
- Operation count only

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
def canonical_operations(document: dict[str, object]) -> set[tuple[str, str, str]]:
    operations: set[tuple[str, str, str]] = set()
    for path, item in document.get("paths", {}).items():
        for method in {"get", "post", "put", "patch", "delete", "options", "head", "trace"}:
            operation = item.get(method)
            if operation:
                operations.add((method.upper(), path, operation["operationId"]))
    return operations

canonical = load_yaml("spec/dist/openapi.bundle.yaml")
observed = app.openapi()
assert canonical_operations(observed) == canonical_operations(canonical)
```

### Why the code is shaped this way

- Operation-set equality is an important gate, but it does not prove parameter, schema, security, or response equivalence.
- FastAPI’s generated document is an observation. Store it as a report; never write it over the canonical source.
- Normalize only explicitly accepted metadata before deeper comparison.
- Use the application through HTTP for validation/error parity; direct function calls bypass adapters.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_framework_validation_is_translated(client, write_headers):
    response = client.post(
        "/analysis-runs",
        headers={**write_headers, "Idempotency-Key": "bad-run-0001"},
        json={"datasetId": 17},
    )

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    payload = response.json()
    assert payload["type"].endswith("/validation")
    assert payload["errors"]
    assert "detail" not in payload or not isinstance(payload["detail"], list)
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Contract-First and Code-First Runtimes check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
await app.ready();
const observed = app.swagger();
const canonical = YAML.parse(await readFile("spec/dist/openapi.bundle.yaml", "utf8"));

const observedOperations = operationSet(observed);
const canonicalOperations = operationSet(canonical);
expect(observedOperations).toEqual(canonicalOperations);

const response = await app.inject({
  method: "POST",
  url: "/analysis-runs",
  headers: { authorization: "Bearer learner-write", "content-type": "application/json" },
  payload: { datasetId: 17 },
});
expect(response.statusCode).toBe(422);
expect(response.headers["content-type"]).toContain("application/problem+json");
```

### Why the code is shaped this way

- `app.swagger()` requires route schemas and the Swagger plugin to be registered before `ready()`.
- The invalid request checks runtime validation; the TypeScript compiler cannot provide this evidence.
- Parse the canonical YAML with a pinned parser and keep generated output out of the source tree unless it is an intentional report.
- Assert stable semantic fields in Problem Details, not framework-specific wording.

### Focused test excerpt

```typescript
it("translates native validation to the public problem contract", async () => {
  const response = await app.inject({
    method: "POST",
    url: "/analysis-runs",
    headers: { ...writeHeaders, "idempotency-key": "bad-run-0001" },
    payload: { datasetId: 17 },
  });

  expect(response.statusCode).toBe(422);
  expect(response.headers["content-type"]).toContain("application/problem+json");
  expect(response.json()).toMatchObject({
    type: "https://api.example.test/problems/validation",
    status: 422,
  });
  expect(response.json<{ errors: unknown[] }>().errors.length).toBeGreaterThan(0);
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Contract-First and Code-First Runtimes, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Contract-First and Code-First Runtimes, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Generated document promoted to canonical | One provider’s annotations silently redefine the API. | Change a FastAPI default and observe the published diff. | Keep generated documents as observations and review against canonical source. |
| Native validation payload leaked | Python and TypeScript return unrelated error bodies. | Send the same malformed identifier to both. | Translate native errors to one Validation Problem schema. |
| Response schema omitted | Stored internal fields appear in JSON. | Inject an owner or fingerprint property into the domain object. | Attach explicit response serializers/models and assert absence. |
| Operation count only | Nineteen routes exist but one method or ID is wrong. | Swap GET and POST or rename one operation ID. | Compare method/path/operationId triples in both directions. |
| Semantic drift allowlisted as formatting | A missing response is suppressed by a broad rule. | Delete 409 and run the comparison. | Restrict allowlists to exact presentational paths and prohibit semantic categories. |
| Provider-specific scenarios | Each implementation passes a different expectation. | Compare the two fixture sets. | Drive both base URLs with the same scenario definitions. |
| Direct-call conformance | Tests bypass headers, serialization, and exception handlers. | Call route functions without an HTTP client. | Retain unit tests, but require live black-box evidence. |
| Coercion mismatch | One provider accepts an ambiguous query value. | Try repeated `limit`, `01`, and `3.0`. | Configure or reject coercion consistently and add regression cases. |

### Defect-injection protocol

Use the module lab to inject the named contract-first and code-first runtimes defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Finish the FastAPI and Fastify providers, compare framework-generated observations to the canonical description, translate framework defaults, and pass one provider-neutral behavioral suite.

This Contract-First and Code-First Runtimes increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/services/python-fastapi/src/analysis_api/`
- `capstone/services/typescript-fastify/src/`
- `capstone/tests/conformance/behavioral-scenarios.yaml`
- `capstone/scripts/run_live_conformance.py`
- `capstone/spec/dist/operation-ledger.json`
- `capstone/reports/`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- complete FastAPI and Fastify providers
- handler-map equality
- generated observation reports
- provider-neutral live conformance

### Commit boundary

The Contract-First and Code-First Runtimes checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.


## Module synthesis

The module answer to “How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior?” is now executable in the capstone: Both providers implement the complete contract and pass one provider-neutral behavioral suite.

## Next in the story

Module 07, [Mocks, Clients, and Contract Testing](../module-07-mocking-clients-contract-testing/index.md), asks: *How do we turn the contract into a development and verification tool rather than a static document?* The current checkpoint must remain green while that new responsibility is added.
