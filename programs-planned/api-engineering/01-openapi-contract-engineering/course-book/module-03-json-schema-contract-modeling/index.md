# Module 03 — JSON Schema Contract Modeling

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How do schemas reject invalid states while remaining usable for providers, clients, and future evolution?

## Where this module fits

Module 02 produced **Complete project and dataset messages, including pagination inputs, creation responses, and problem representations**. This module extends that result by asking: **How do schemas reject invalid states while remaining usable for providers, clients, and future evolution?**

The new capstone increment is **Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus**. It becomes the prerequisite for **References and Multi-Document Architecture**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish missing, null, empty, and default.
- Constrain objects, arrays, strings, and numbers precisely.
- Use composition as logic rather than inheritance.
- Design tagged unions and separate input/output models.
- Verify a shared corpus of valid and invalid instances.

## Capstone increment

Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus.

## Core model

### Driving question

> Which JSON instances are legal, and which states must be impossible?

### Observable outcome

Model project, dataset, run, artifact, and problem representations with explicit absence, nullability, closure, constraints, unions, and independent fixtures.

### 1. A schema denotes a set of instances

Treat every schema as a set: validation answers whether an instance belongs. `maxLength: 80` removes longer strings from the set; `required: [name]` removes objects without `name`; `additionalProperties: false` removes objects with unknown keys. This model is more precise than saying a schema “looks like a class.”

### 2. Presence, nullability, emptiness, and defaults are separate

A property absent from an object is not the same instance as a property present with `null`, `""`, `[]`, or `{}`. A property can be required and nullable, optional and non-null, or optional and nullable. JSON Schema `default` is an annotation; validators are not required to insert it.

The capstone response models often require nullable server fields such as `completedAt` so the shape is stable across states. Creation models omit server-owned fields entirely. Tests cover each absence/null boundary.
### 3. Object closure is a compatibility decision

Without an applicator restricting extra properties, object schemas generally allow unknown members. Closing request objects detects typos and over-posting. Closing response objects prevents unreviewed fields from leaking but can make additive evolution harder for strict consumers.

The capstone closes domain objects and uses explicit maps where arbitrary keys are intended, such as run labels. This is a conscious contract policy, not a universal JSON Schema best practice.
### 4. Composition is logic, not inheritance

`allOf` means every subschema must validate; `anyOf` means at least one; `oneOf` means exactly one; `not` excludes a set. These are logical applicators. Using `allOf` merely to imitate object-oriented inheritance often creates surprising closure and requiredness behavior.

For dataset sources, two tagged alternatives with distinct `const` values make `oneOf` exclusive. The tag is useful to humans and generators, while the validation truth still comes from the schemas.
### 5. Formats are annotations unless assertion is enabled

JSON Schema defines format vocabularies, but an implementation can collect `format` as annotation without rejecting invalid strings. OpenAPI tooling also varies. A contract that requires a valid date-time or URI must state its enforcement policy and test the selected validators.

The course’s independent validator uses a format checker, and both providers configure formats needed by their runtime schemas. Capability differences are evidence, not reasons to assume validation occurred.
### 6. Input and output models serve different trust directions

Creation input should not accept `id`, `ownerId`, timestamps, version counters, artifact IDs, or status chosen by the server. Response models should include the server-owned fields consumers need. Reusing one broad schema in both directions creates over-posting or optionalizes essential response data.

`readOnly` and `writeOnly` annotations help documentation and generators, but explicit `ProjectCreate`, `ProjectPatch`, and `Project` schemas make the allowed sets unambiguous across tools.
### 7. Static types do not validate JSON

A TypeScript type is erased at runtime, and a Python annotation does not validate arbitrary network bytes by itself. Runtime libraries must parse and validate. Generated types can still misrepresent unions, formats, or additional properties, so fixtures are run through an independent JSON Schema validator and both provider boundaries.

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

1. List the four distinct instances for a `description` property: missing, null, empty, non-empty.
2. Design required-but-nullable `completedAt`.
3. Why does `default: normal` not guarantee the provider receives `priority`?
4. Create an instance that would expose overlapping local/remote source branches.
5. When is `additionalProperties` a schema rather than `false`?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For JSON Schema 2020-12 Contract Modeling, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| OpenAPI 3.1 Schema Objects use the JSON Schema 2020-12 dialect with OAS vocabulary additions. | OAS/JSON Schema model | Keywords should be interpreted with modern JSON Schema semantics. | baseline root and validator configuration |
| `required` applies to object property presence, not nullability. | JSON Schema semantics | Missing and present-null must be tested separately. | fixture corpus |
| `oneOf` succeeds only when exactly one branch validates. | JSON Schema semantics | Overlapping alternatives make otherwise plausible instances invalid. | union fixtures |
| `default` does not require a validator to mutate the instance. | JSON Schema semantics | Provider defaulting is separate implementation behavior. | request/response tests |
| Domain request and response objects are closed unless they intentionally model a map. | course policy | Typos, over-posting, and leakage fail early. | unknown-property fixtures |
| Every canonical schema has valid and invalid examples or fixtures. | course evidence policy | A schema without boundary cases is not reviewed deeply enough. | `make -C capstone fixtures` |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every JSON Schema 2020-12 Contract Modeling claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the JSON Schema 2020-12 Contract Modeling document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
DatasetCreate:
  type: object
  additionalProperties: false
  required: [name, source]
  properties:
    name:
      type: string
      minLength: 1
      maxLength: 100
    source:
      oneOf:
        - $ref: ./LocalFileSource.yaml
        - $ref: ./RemoteObjectSource.yaml
      discriminator:
        propertyName: kind

LocalFileSource:
  type: object
  additionalProperties: false
  required: [kind, fileName, mediaType]
  properties:
    kind:
      const: local-file
    fileName:
      type: string
      minLength: 1
      maxLength: 255
    mediaType:
      enum: [text/csv, application/json, application/octet-stream]

RemoteObjectSource:
  type: object
  additionalProperties: false
  required: [kind, uri]
  properties:
    kind:
      const: remote-object
    uri:
      type: string
      format: uri
      pattern: '^https://objects\.example\.test/[^?#\s]+$'
```

### Close reading

- `oneOf` is sound because `kind` cannot satisfy both `const` constraints.
- Closure belongs on each branch; closing only the outer `DatasetCreate` object does not close the nested source object.
- The discriminator aids selection but does not replace validation of branch constraints.
- `format: uri` is paired with a policy pattern that narrows the training source host; each has a different purpose.
- No response-owned identifier or status appears in `DatasetCreate`.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Optional confused with nullable
- Default treated as insertion
- Overlapping oneOf
- Open object by accident

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
class LocalFileSource(ContractModel):
    kind: Literal["local-file"]
    file_name: str = Field(alias="fileName", min_length=1, max_length=255)
    media_type: Literal["text/csv", "application/json", "application/octet-stream"] = Field(alias="mediaType")

class RemoteObjectSource(ContractModel):
    kind: Literal["remote-object"]
    uri: str = Field(pattern=r"^https://objects\.example\.test/[^?#\s]+$")
    checksum_sha256: str | None = Field(alias="checksumSha256", default=None, pattern=r"^[a-f0-9]{64}$")

DatasetSource = Annotated[LocalFileSource | RemoteObjectSource, Field(discriminator="kind")]

class DatasetCreate(ContractModel):
    name: str = Field(min_length=1, max_length=100)
    source: DatasetSource
```

### Why the code is shaped this way

- `ContractModel` forbids unknown properties and emits aliases so runtime behavior follows the closed public schema.
- Pydantic’s discriminated union is an implementation of the same tagged-set decision; fixtures guard against library-specific widening.
- URI format validation and host policy require explicit validators if a simple pattern is insufficient.
- Use `model_dump(by_alias=True)` at the boundary so public property names do not drift to snake_case.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_closed_input_rejects_over_posting_without_mutation(client, write_headers):
    before = client.get("/projects", headers=write_headers).json()["items"]
    response = client.post(
        "/projects",
        headers=write_headers,
        json={"name": "Injected", "ownerId": "attacker"},
    )

    assert response.status_code == 422
    assert response.json()["errors"]
    after = client.get("/projects", headers=write_headers).json()["items"]
    assert after == before
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused JSON Schema Contract Modeling check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
export const DatasetSourceSchema = Type.Union([
  Type.Object(
    {
      kind: Type.Literal("local-file"),
      fileName: Type.String({ minLength: 1, maxLength: 255 }),
      mediaType: Type.Union([
        Type.Literal("text/csv"),
        Type.Literal("application/json"),
        Type.Literal("application/octet-stream"),
      ]),
    },
    { additionalProperties: false },
  ),
  Type.Object(
    {
      kind: Type.Literal("remote-object"),
      uri: Type.String({
        format: "uri",
        pattern: "^https://objects\\.example\\.test/[^?#\\s]+$",
      }),
      checksumSha256: Type.Optional(
        Type.String({ pattern: "^[a-f0-9]{64}$" }),
      ),
    },
    { additionalProperties: false },
  ),
]);
```

### Why the code is shaped this way

- `Type.Union` produces runtime JSON Schema and a static type, but generator/runtime agreement is still tested with the shared fixtures.
- A union of objects without distinct literal tags can overlap and make `oneOf` semantics hard to preserve across tools.
- Ajv format support depends on configuration and plugins; the course tests it instead of trusting the static TypeBox declaration.
- Closed nested objects reject unknown input before it reaches the store.

### Focused test excerpt

```typescript
it("rejects an undeclared owner field before mutation", async () => {
  const response = await app.inject({
    method: "POST",
    url: "/projects",
    headers: writeHeaders,
    payload: { name: "Injected", ownerId: "attacker" },
  });

  expect(response.statusCode).toBe(422);
  expect(response.json<{ errors: unknown[] }>().errors.length).toBeGreaterThan(0);
  const page = await app.inject({ method: "GET", url: "/projects", headers: writeHeaders });
  expect(page.json<{ items: unknown[] }>().items).toHaveLength(0);
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For JSON Schema 2020-12 Contract Modeling, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For JSON Schema 2020-12 Contract Modeling, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Optional confused with nullable | A property is omitted from `required` when the intent was required-but-nullable. | Compare `{}` with `{"completedAt": null}`. | Model presence and type independently. |
| Default treated as insertion | A schema default is expected to mutate requests. | Validate an instance missing the property and inspect it afterward. | Default in provider code deliberately or require the field; document behavior. |
| Overlapping oneOf | Both branches accept an object, so exactly-one validation fails. | Create an instance satisfying both branches. | Add distinguishable const tags or change the logical relation. |
| Open object by accident | A typo such as `fileNme` is accepted. | Add an unknown property fixture. | Set closure deliberately at the correct object level. |
| allOf inheritance trap | Closed base and extension schemas reject each other’s properties. | Validate the composed object with fields from both. | Design the full object set or use modern unevaluated-property semantics carefully. |
| Format assumed enforced | Invalid date-time passes one validator. | Run the same fixture through every selected validator. | Configure assertion or add explicit semantic validation. |
| Server-owned over-posting | Creation accepts `ownerId` or `status`. | Submit those properties and observe acceptance. | Separate input/output schemas and close input. |

### Defect-injection protocol

Use the module lab to inject the named json schema contract modeling defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Model project, dataset, run, artifact, and problem representations with explicit absence, nullability, closure, constraints, unions, and independent fixtures.

This JSON Schema 2020-12 Contract Modeling increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/components/schemas/`
- `capstone/tests/fixtures/schema/manifest.yaml`
- `capstone/tests/fixtures/schema/valid/`
- `capstone/tests/fixtures/schema/invalid/`
- `capstone/services/python-fastapi/src/analysis_api/models.py`
- `capstone/services/typescript-fastify/src/schemas.ts`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- closed domain schema set
- 67-case shared fixture corpus
- input/output model separation
- validator agreement report

### Commit boundary

The JSON Schema 2020-12 Contract Modeling checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Distinguish missing, null, empty, and default, Constrain objects, arrays, strings, and numbers precisely, and Use composition as logic rather than inheritance** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Plant an overlapping union branch, observe the independent failure, and repair it without weakening closure** and requiring the following oracle: **at least 60 fixtures cover valid and invalid boundaries; missing and null are independent; domain objects are closed; intentional maps have bounded value schemas.**

The cumulative platform now includes **Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [References and Multi-Document Architecture](../module-04-references-multi-document-architecture/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
