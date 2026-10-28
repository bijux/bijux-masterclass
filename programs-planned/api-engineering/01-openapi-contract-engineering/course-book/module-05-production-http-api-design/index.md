# Module 05 — Production HTTP API Design

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures?

## Where this module fits

Module 04 produced **Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles**. This module extends that result by asking: **How should an HTTP API express asynchronous work, retries, conflicts, conditional updates, and machine-readable failures?**

The new capstone increment is **Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details**. It becomes the prerequisite for **Contract-First and Code-First Runtimes**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Use `202 Accepted` with a status resource.
- Define idempotency-key behavior precisely.
- Use ETags and preconditions for optimistic concurrency.
- Design stable pagination and lifecycle-aware errors.
- Use RFC 9457 Problem Details as a public error vocabulary.

## Capstone increment

Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details.

## Core model

### Driving question

> How does the contract express retries, concurrency, long-running work, pagination, and failures?

### Observable outcome

Add asynchronous analysis runs, idempotent submission, conditional updates, cursor pagination, cancellation, artifacts, and one coherent Problem Details vocabulary.

### 1. Asynchronous acceptance is not completion

`202 Accepted` says the request was accepted for processing but processing is not complete. A useful response identifies how the client can observe status—here, a run resource in `Location` plus a current run representation and `Retry-After` guidance.

Returning 202 and then losing the job is still possible; HTTP does not guarantee execution. The contract must describe observable lifecycle states and failures. The deterministic training provider advances on polling so protocol behavior is testable without a queue.
### 2. Idempotency is an operation protocol

POST can be made safely retryable through an application-level idempotency key. The server scopes the key to a principal, binds it to a canonical request-body fingerprint, stores the logical result, and replays it for the same request. A changed body under the key is a conflict.

Merely checking whether an identical resource already exists is not the same guarantee. Keys need length, character, retention, replay, and mismatch behavior in the contract.
### 3. Conditional requests prevent lost updates

An entity tag identifies a selected representation version. The client sends `If-Match` with the tag it observed. If the current tag differs, the server returns `412 Precondition Failed` rather than overwriting another update. If the contract requires a precondition and none is supplied, `428 Precondition Required` makes that policy explicit.

ETags are opaque to clients even when the training implementation encodes an ID and version for readability.
### 4. Pagination is a consistency and cost contract

Offset pagination is easy to understand but unstable under insertions and deletions. Cursor pagination can encode a stable continuation position but makes random access harder. The capstone uses a simple numeric cursor for deterministic teaching and bounds page size to 50.

A page schema includes items and a nullable `nextCursor`. Filters apply before slicing. Clients must treat cursors as opaque despite the training representation.
### 5. Problem Details standardizes the envelope, not every problem

The common fields—type, title, status, detail, instance—give generic clients a stable structure. The API still chooses stable problem type identifiers and defines when to use 404, 409, 412, 413, 415, 422, or 428. Validation extends the shape with structured issues.

Do not expose exception class names, stack traces, SQL text, or mutable human messages as machine identifiers. Branch on status and stable type, not exact prose.
### 6. State transitions are part of the public model

Queued and running runs can be canceled; completed, failed, and canceled runs are terminal. Artifacts are unavailable before completion. These rules determine legal responses and conflict branches, so they belong in the contract narrative, examples, and tests—not only the store implementation.
### 7. Retries require classifying failures

A client might retry transient server failures, honor `Retry-After`, correct validation input, refresh authentication, or abandon a conflict. The status code alone is not a universal retry algorithm, but careless status selection removes useful signals.

The course asks for retry reasoning on every operation: method semantics, idempotency mechanism, preconditions, and side effects.

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

1. Why is 202 different from 201?
2. Specify idempotency behavior for same key/same body and same key/different body.
3. Why scope idempotency keys by principal?
4. What does an ETag mean to a client?
5. Distinguish 409 and 412 in this API.

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Production HTTP API Design, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| `202` responses identify a status monitor and do not claim completion. | HTTP semantics plus course design | Consumers need an observable continuation. | Location/representation assertions |
| Same principal, key, and body produce the same logical run. | course idempotency contract | Network retries must not duplicate analysis. | retry-storm test |
| Same principal and key with a different body returns 409. | course idempotency contract | A key cannot ambiguously name two intents. | negative replay test |
| Project mutation requires `If-Match`; stale tags return 412 and missing tags 428. | course concurrency policy | Lost updates become detectable. | conditional-update tests |
| Problem responses use stable type identifiers and `application/problem+json`. | RFC 9457-based course policy | Generic and domain-specific consumers share an envelope. | live content-type/schema checks |
| Terminal run states never transition and incomplete runs expose no artifacts. | domain invariant | Lifecycle behavior remains deterministic and safe. | state-machine tests |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Production HTTP API Design claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Production HTTP API Design document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
/analysis-runs:
  post:
    operationId: createAnalysisRun
    parameters:
      - $ref: ../components/parameters/IdempotencyKey.yaml
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: ../components/schemas/AnalysisRunCreate.yaml
    responses:
      '202':
        description: Analysis accepted but not complete
        headers:
          Location:
            $ref: ../components/headers/Location.yaml
          Retry-After:
            $ref: ../components/headers/RetryAfter.yaml
          Idempotent-Replay:
            $ref: ../components/headers/IdempotentReplay.yaml
        content:
          application/json:
            schema:
              $ref: ../components/schemas/AnalysisRun.yaml
          links:
            status:
              operationId: getAnalysisRun
              parameters:
                runId: '$response.body#/id'
      '409':
        $ref: ../components/responses/Conflict.yaml
      '422':
        $ref: ../components/responses/ValidationProblem.yaml
```

### Close reading

- The accepted representation may show `queued`; no completed artifact is implied.
- `Location` and the link both point consumers toward `getAnalysisRun`, but one is HTTP metadata and the other is OpenAPI relationship metadata.
- `Idempotent-Replay` distinguishes original acceptance from a replay without changing the logical run.
- `409` covers a key/body mismatch or incompatible resource lifecycle; stable problem types distinguish subcases.
- The key is a header parameter because it controls request processing rather than domain representation.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- 202 without monitor
- Key not bound to body
- Check-then-create race
- Last-write-wins patch

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
def create_run(self, owner: str, admin: bool, key: str, body: AnalysisRunCreate) -> tuple[AnalysisRun, bool]:
    fingerprint = hashlib.sha256(
        json.dumps(body.model_dump(by_alias=True, mode="json"), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    record_key = (owner, key)
    existing = self.idempotency.get(record_key)
    if existing:
        if existing.fingerprint != fingerprint:
            raise ApiProblem(409, "Request conflict", "The idempotency key was used with another body.", "idempotency-conflict")
        return self.runs[existing.run_id], True
    run = self._new_run(owner, body)
    self.idempotency[record_key] = IdempotencyRecord(fingerprint, run.id)
    return run, False
```

### Why the code is shaped this way

- Canonical JSON ordering makes semantically equivalent object-key order produce the same fingerprint; list order remains meaningful.
- Persistence and atomicity would be required in production. The in-memory lock makes the training claim precise within one process.
- The adapter converts replay boolean into a response field and always returns 202 for the same accepted operation.
- Add a concurrent or repeated-request test, not only two sequential direct method calls.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_idempotency_key_is_bound_to_request_body(client, write_headers):
    project_id, dataset_id = create_ready_dataset(client, write_headers)
    headers = {**write_headers, "Idempotency-Key": "run-retry-0001"}
    body = {
        "projectId": project_id,
        "datasetId": dataset_id,
        "parameters": {"algorithm": "quality-summary"},
    }

    first = client.post("/analysis-runs", headers=headers, json=body)
    replay = client.post("/analysis-runs", headers=headers, json=body)
    changed = client.post(
        "/analysis-runs",
        headers=headers,
        json={**body, "parameters": {"algorithm": "checksum"}},
    )

    assert first.status_code == replay.status_code == 202
    assert first.json()["id"] == replay.json()["id"]
    assert replay.headers["idempotent-replay"] == "true"
    assert changed.status_code == 409
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Production HTTP API Design check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
const key = `${principal.subject}\0${idempotencyKey}`;
const existing = this.idempotency.get(key);
const fingerprint = createHash("sha256").update(canonical(body)).digest("hex");
if (existing) {
  if (existing.fingerprint !== fingerprint) {
    throw new ApiProblem(409, "Request conflict", "The idempotency key was already used with a different request body.", "idempotency-conflict");
  }
  return { run: this.runs.get(existing.runId)!, replay: true };
}
const run = this.createFreshRun(principal, body);
this.idempotency.set(key, { fingerprint, runId: run.id });
return { run, replay: false };
```

### Why the code is shaped this way

- Provider parity depends on using the same canonicalization rules and key scope, not merely similar code structure.
- In a distributed provider, this record needs an atomic unique constraint or transactional claim; process-local maps are explicitly limited.
- Never use the idempotency key itself as a resource ID or echo it into logs without redaction policy.
- The shared live suite sends the same body twice and a changed body once.

### Focused test excerpt

```typescript
it("replays the same idempotent request and rejects a changed body", async () => {
  const { projectId, datasetId } = await createReadyDataset(app);
  const headers = { ...writeHeaders, "idempotency-key": "run-retry-0001" };
  const payload = { projectId, datasetId, parameters: { algorithm: "quality-summary" } };

  const first = await app.inject({ method: "POST", url: "/analysis-runs", headers, payload });
  const replay = await app.inject({ method: "POST", url: "/analysis-runs", headers, payload });
  const changed = await app.inject({
    method: "POST",
    url: "/analysis-runs",
    headers,
    payload: { ...payload, parameters: { algorithm: "checksum" } },
  });

  expect(first.statusCode).toBe(202);
  expect(replay.json<{ id: string }>().id).toBe(first.json<{ id: string }>().id);
  expect(replay.headers["idempotent-replay"]).toBe("true");
  expect(changed.statusCode).toBe(409);
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Production HTTP API Design, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Production HTTP API Design, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| 202 without monitor | Response says accepted but gives no status URI or representation. | Disconnect after the response and ask how a client continues. | Return Location/link and model a status resource. |
| Key not bound to body | Same key silently replays a different request. | Reuse a key with changed algorithm. | Store and compare a canonical request fingerprint. |
| Check-then-create race | Concurrent retries both see no record and create runs. | Issue parallel requests around the check. | Use atomic persistence/locking; document training scope. |
| Last-write-wins patch | Two clients update from the same version and one overwrites the other. | Send two patches with one observed ETag. | Require If-Match and return 412 to the stale request. |
| Conflict collapsed into validation | A ready-state or idempotency conflict returns 422. | Send schema-valid input in an illegal lifecycle state. | Use 409 and a stable problem type. |
| Artifacts before completion | Listing artifacts returns an empty 200 for a queued run. | Start then immediately list. | Return a documented 409 until completion. |
| Mutable problem identity | Clients branch on English detail text. | Change wording and observe consumer failure. | Use stable type URI/status/code for machine behavior. |

### Defect-injection protocol

Use the module lab to inject the named production http api design defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Add asynchronous analysis runs, idempotent submission, conditional updates, cursor pagination, cancellation, artifacts, and one coherent Problem Details vocabulary.

This Production HTTP API Design increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/paths/analysis-runs.yaml`
- `capstone/spec/paths/analysis-run.yaml`
- `capstone/spec/paths/analysis-run-cancellation.yaml`
- `capstone/spec/paths/analysis-run-artifacts.yaml`
- `capstone/spec/components/schemas/AnalysisRun.yaml`
- `capstone/spec/components/schemas/Problem.yaml`
- `capstone/services/python-fastapi/src/analysis_api/store.py`
- `capstone/services/typescript-fastify/src/store.ts`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- asynchronous run lifecycle
- idempotency and conditional-write tests
- Problem Details catalog
- pagination/state-transition evidence

### Commit boundary

The Production HTTP API Design checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Use `202 Accepted` with a status resource, Define idempotency-key behavior precisely, and Use ETags and preconditions for optimistic concurrency** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant a race-prone check-then-create implementation or remove the fingerprint check; prove a focused test fails, then repair it** and requiring the following oracle: **202 identifies status monitoring; same key/body creates one logical run; changed body under key is rejected; missing/stale/current If-Match branches are distinct.**

The cumulative platform now includes **Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Contract-First and Code-First Runtimes](../module-06-contract-first-code-first-runtime/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
