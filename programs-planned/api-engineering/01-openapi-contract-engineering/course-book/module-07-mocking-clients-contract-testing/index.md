# Module 07 — Mocks, Clients, and Contract Testing

Prism is excluded from the installable toolchain because its dependency chain
has unresolved security advisories. Mock/proxy lessons and fixtures remain as
reference material. `make prism-mock` and `make prism-smoke` stop with an explicit
error; `npm run mock` and `npm run proxy:python` are unavailable. Full course
qualification remains blocked until a maintained replacement is qualified.

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How do mocks, generated clients, examples, property tests, and stateful tests provide different evidence?

## Where this module fits

Module 06 produced **Map every operation to both providers and compare generated observations with the canonical contract**. This module extends that result by asking: **How do mocks, generated clients, examples, property tests, and stateful tests provide different evidence?**

The new capstone increment is **Build the consumer and contract-test ladder against the mock and both real providers**. It becomes the prerequisite for **Security in the Public Contract**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish syntax, semantic linting, conformance, and consumer tests.
- Develop consumers against a mock without mistaking examples for complete behavior.
- Generate and review clients in Python and TypeScript.
- Use generated and property-based tests to explore boundaries.
- Record tool capability limits instead of hiding them.

## Capstone increment

Build the consumer and contract-test ladder against the mock and both real providers.

## Core model

### Driving question

> How does a static contract become an executable development and verification system?

### Observable outcome

Build the verification ladder: lint and bundle, run a contract mock, generate Python and TypeScript consumers, execute shared workflows, and use generated property/stateful tests to find defects beyond examples.

### 1. Each tool proves a bounded claim

A parser proves that a document can be read. A linter applies structural and organizational rules. A bundler resolves references into a publication artifact. A mock simulates responses from examples or schemas. A generator maps the contract into consumer code. A contract tester sends generated requests to a live provider. These claims overlap, but none means “the API is correct.”

The lab records which artifact, provider, and tool version produced each result. Tool output without a stated claim becomes ceremony. A green mock, for example, proves the consumer can speak to the mock—not that the real provider has the same state transitions.
### 2. Lint policy should encode expensive review knowledge

Built-in lint rules catch common OpenAPI mistakes. Organizational rules should target defects repeatedly seen in reviews: missing `operationId`, absent explicit security decision, response without media type, undocumented 4xx classes, weak descriptions, or unstable naming. Rules should not become a prose-style bureaucracy.

Every custom rule needs a rationale, positive fixture, negative fixture, and migration path. A rule that cannot explain the consumer or operational risk should remain guidance rather than a blocking gate.
### 3. Mocks decouple consumer work but can create false confidence

A contract mock lets consumers develop before a provider exists and makes examples executable. Dynamic schema-generated responses broaden coverage, while explicit examples make domain stories legible. Both can be misleading when examples encode impossible lifecycle state or when the mock does not enforce requests.

The capstone runs the same consumer workflow against Prism and real providers where supported. State-dependent steps are marked when a generic mock cannot persist resource identity. The limitation is reported rather than hidden behind a fabricated all-green workflow.
### 4. Generated clients are compiled interpretations

A generator chooses method names, parameter grouping, nullable conventions, error surfaces, and transport abstractions. Generation success does not mean the resulting client is ergonomic or semantically complete. A change in `operationId` can be a source-breaking change even when the wire endpoint is unchanged.

The course keeps thin handwritten workflow clients plus generator snapshots. Generated output is reproducible and disposable; review focuses on generator configuration, contract inputs, compile checks, and a small consumer acceptance suite rather than hand-editing emitted files.
### 5. Static types do not validate remote responses

A generated Python model or TypeScript interface describes what code expects. The remote server can still return invalid data. Some clients validate responses; many only deserialize or cast. Consumers need a policy: trust a controlled provider, validate at boundaries, or selectively validate high-risk operations.

The labs deliberately return a malformed response from a stub and observe what each generated stack does. The capability matrix records whether response validation is generated, optional, or absent.
### 6. Property-based testing explores schema boundaries

Examples cover named cases. Property-based contract testing derives many legal and illegal values from constraints: minimum and maximum lengths, numeric bounds, patterns, enums, nested combinations, missing required fields, and unexpected properties. Shrinking reduces a complex failure to a minimal reproducer.

Generated tests are strongest when schemas are precise. An unconstrained string produces noise rather than meaningful coverage. Tool failures can reveal provider defects, contract ambiguity, or unsupported schema features; triage must classify which one occurred.
### 7. Negative testing must be intentional

A provider that accepts every payload can pass a happy-path suite. Negative tests ask whether malformed identifiers, unknown enums, illegal extra fields, wrong media types, missing credentials, and boundary overflow are rejected with the documented public problem.

Do not assert only “not 500.” Assert the expected client-error class, media type, stable problem identity, and absence of unintended state mutation. A rejected create request must not leave a project or run behind.
### 8. Stateful testing derives operation sequences

Many failures appear only after a sequence: update after delete, cancel after completion, retrieve another owner’s artifact, reuse an idempotency key with a changed body, or follow a link using a captured identifier. Stateful tools use explicit links, inferred relationships, or custom state machines to construct these paths.

The capstone supplies a deterministic baseline sequence and adds generated exploration around it. State reset, credentials, and data cleanup are part of the test contract; otherwise failures cannot be reproduced.
### 9. Seeds, examples, and reports make generation auditable

Randomized testing is useful only when a failure can be replayed. Preserve the minimized request, seed, tool version, contract digest, provider revision, and response. Promote important minimized cases into permanent fixtures rather than relying on the generator to rediscover them.

A report should separate tool crash, invalid generated request, provider mismatch, and documented rejection. “Schemathesis failed” is not a diagnosis.
### 10. Capability gaps are engineering facts

No generator or mock implements every OpenAPI and JSON Schema feature uniformly. A mature toolchain probes support for callbacks, links, multipart encodings, discriminated unions, 3.2 fields, and sequential media. Unsupported features receive a documented fallback, a manual test, or a pinned exclusion with risk.

Silently dropping an operation or schema keyword is unacceptable. The course’s capability report uses four states: supported, partially supported, transformed, and unsupported, each tied to executed evidence where the environment permits.

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

1. What does a successful bundle prove?
2. When should a custom lint rule block CI?
3. Why retain examples when property generation exists?
4. What should happen when a generator omits callbacks?
5. How do you test that rejection caused no mutation?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Linting, Mocking, Clients, and Contract Testing, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Lint, bundle, example validation, mock, generation, and live testing remain separate proof stages. | evidence policy | A single green tool cannot justify claims outside its capability. | proof ladder report |
| Custom blocking lint rules have positive and negative fixtures. | quality policy | Rules must be testable and avoid arbitrary review bureaucracy. | Spectral fixture exercise |
| Generated clients are reproducible from the canonical bundled input and pinned generator versions. | build policy | Hand-edited generated code is not maintainable evidence. | client generation targets |
| Every generated-test failure preserves a reproducer or seed before repair. | testing policy | Nondeterministic failures cannot become regression evidence. | reports and promoted fixtures |
| Negative tests assert both rejection and absence of unintended mutation. | correctness rule | A 4xx response can still hide partial side effects. | provider and live tests |
| Unsupported tool features are named in the capability matrix and covered by another verification where material. | honesty rule | Silent feature loss creates false assurance. | capability report |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Linting, Mocking, Clients, and Contract Testing claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Linting, Mocking, Clients, and Contract Testing document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
post:
  operationId: createAnalysisRun
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: ../components/schemas/AnalysisRunCreate.yaml
        examples:
          standard:
            value:
              datasetId: dat_0001
              algorithm: quality-summary
  responses:
    '202':
      description: Analysis was accepted
      headers:
        Location:
          $ref: ../components/headers/Location.yaml
      content:
        application/json:
          schema:
            $ref: ../components/schemas/AnalysisRun.yaml
          links:
            status:
              operationId: getAnalysisRun
              parameters:
                runId: $response.body#/id
```

### Close reading

- The named example is validated against the request schema and can drive mock and documentation behavior.
- The link expresses a machine-readable relationship from the accepted representation to the status operation.
- `operationId` stability directly affects generated method names and link resolution.
- Links do not force a client generator to implement workflow orchestration; capability must be tested.
- The response still needs live assertions for Location syntax, body/link consistency, and lifecycle behavior.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Lint equals correctness
- Mock-only confidence
- Generated type trusted at runtime
- Generator warning ignored

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
with AnalysisApiClient(base_url=base_url, token="learner-write") as client:
    project = client.create_project(name="contract-lab")
    dataset = client.register_dataset(project.id, name="reads.fastq")
    client.upload_dataset_content(dataset.id, b"@r1\nACGT\n+\n!!!!\n")
    run = client.create_analysis_run(
        dataset_id=dataset.id,
        algorithm="quality-summary",
        idempotency_key="module-07-workflow",
    )
    completed = client.wait_for_terminal(run.id, max_attempts=5)
    assert completed.status == "completed"
    assert client.list_artifacts(run.id)
```

### Why the code is shaped this way

- The workflow client is intentionally thin: transport, typed public data, problem parsing, polling policy, and no hidden provider imports.
- Use a generated SDK in a parallel acceptance test; keep this handwritten client as a stable teaching reference.
- Polling has a bounded attempt count and interprets Retry-After rather than sleeping indefinitely.
- Tests can point the same client at a mock or either provider, with stateful limitations recorded.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_handwritten_consumer_completes_the_outcome(running_provider):
    with AnalysisApiClient(base_url=running_provider, token="learner-write") as client:
        project = client.create_project(name="consumer proof")
        dataset = client.register_local_dataset(project.id, name="reads.csv")
        client.upload_dataset_content(dataset.id, b"sample,value\nA,1\n", "text/csv")
        run = client.create_analysis_run(
            project_id=project.id,
            dataset_id=dataset.id,
            algorithm="quality-summary",
            idempotency_key="consumer-proof-0001",
        )
        terminal = client.wait_for_terminal(run.id, max_attempts=5)
        assert terminal.status == "completed"
        assert client.list_artifacts(run.id).items
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Mocks, Clients, and Contract Testing check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
const client = new AnalysisApiClient({ baseUrl, token: "learner-write" });
const project = await client.createProject({ name: "contract-lab" });
const dataset = await client.registerDataset(project.id, {
  name: "reads.fastq",
  source: { kind: "local-file", fileName: "reads.fastq", mediaType: "application/octet-stream" },
});
await client.uploadDatasetContent(
  dataset.id,
  new TextEncoder().encode("@r1\nACGT\n+\n!!!!\n"),
);
const run = await client.createAnalysisRun(
  {
    projectId: project.id,
    datasetId: dataset.id,
    parameters: { algorithm: "quality-summary" },
  },
  "module-07-workflow",
);
const completed = await client.waitForTerminal(run.id, { maxAttempts: 5 });
if (completed.status !== "completed") throw new Error(`unexpected ${completed.status}`);
```

### Why the code is shaped this way

- Runtime responses are parsed through a narrow validation/assertion layer rather than cast blindly to generated interfaces.
- The idempotency key is a call argument because retry identity belongs to request execution, not the domain body.
- Generated `openapi-typescript` declarations are compiled separately to expose contract-to-type mapping errors.
- Consumer tests assert Problem Details for non-2xx responses instead of reducing every error to a string.

### Focused test excerpt

```typescript
it("completes the consumer outcome through the public client", async () => {
  const client = new AnalysisApiClient({ baseUrl, token: "learner-write" });
  const project = await client.createProject({ name: "consumer proof" });
  const dataset = await client.registerDataset(project.id, {
    name: "reads.csv",
    source: { kind: "local-file", fileName: "reads.csv", mediaType: "text/csv" },
  });
  await client.uploadDatasetContent(dataset.id, new TextEncoder().encode("sample,value\nA,1\n"));
  const run = await client.createAnalysisRun(
    { projectId: project.id, datasetId: dataset.id, parameters: { algorithm: "quality-summary" } },
    "consumer-proof-0001",
  );
  expect((await client.waitForTerminal(run.id, { maxAttempts: 5 })).status).toBe("completed");
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Linting, Mocking, Clients, and Contract Testing, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Linting, Mocking, Clients, and Contract Testing, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Lint equals correctness | A perfectly styled contract is assumed to match runtime. | Change provider status while lint remains green. | Keep live conformance as a separate gate. |
| Mock-only confidence | Consumer passes against examples but real provider rejects the request. | Run identical call against both targets. | Use mock for decoupling, then provider acceptance. |
| Generated type trusted at runtime | Malformed JSON is cast to the expected interface. | Stub a missing required response field. | Add response validation or explicit trust policy. |
| Generator warning ignored | An operation or union is skipped silently. | Inspect generated operation ledger and build logs. | Fail on unsupported material features or add a manual adapter/test. |
| Random failure lost | A generated defect cannot be replayed. | Rerun without seed/report. | Persist minimized example, seed, versions, and contract digest. |
| Negative request mutates state | Provider validates after creating a record. | Compare collection before and after rejected create. | Validate before mutation and assert no side effect. |
| Stateful suite has dirty state | Order-dependent failures appear intermittently. | Reverse or repeat tests. | Use isolated provider state or explicit reset/unique data. |
| Every 4xx treated alike | Authorization, validation, and conflict regressions go unnoticed. | Change one status/media type. | Assert exact documented class and problem identity. |

### Defect-injection protocol

Use the module lab to inject the named mocks, clients, and contract testing defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Build the verification ladder: lint and bundle, run a contract mock, generate Python and TypeScript consumers, execute shared workflows, and use generated property/stateful tests to find defects beyond examples.

This Linting, Mocking, Clients, and Contract Testing increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/.spectral.yaml`
- `capstone/redocly.yaml`
- `capstone/clients/python/`
- `capstone/clients/typescript/`
- `capstone/scripts/prism_smoke.py`
- `capstone/scripts/client_view.py`
- `capstone/schemathesis.toml`
- `capstone/tests/fixtures/schema/`
- `capstone/reports/`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- lint policy fixtures
- Prism mock smoke route
- Python and TypeScript consumers
- generated/property/stateful evidence

### Commit boundary

The Linting, Mocking, Clients, and Contract Testing checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Distinguish syntax, semantic linting, conformance, and consumer tests, Develop consumers against a mock without mistaking examples for complete behavior, and Generate and review clients in Python and TypeScript** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Run generated property tests with bounded cases and deterministic reporting; classify every failure** and requiring the following oracle: **custom rules have passing/failing fixtures; mock requests are validated; both generated clients build or import; consumer workflow runs against real providers.**

The cumulative platform now includes **Build the consumer and contract-test ladder against the mock and both real providers**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Security in the Public Contract](../module-08-security-authentication-authorization/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
