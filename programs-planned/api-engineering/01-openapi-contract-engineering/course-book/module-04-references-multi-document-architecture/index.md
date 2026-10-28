# Module 04 — References and Multi-Document Architecture

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How can a multi-document contract remain understandable, relocatable, and deterministically buildable?

## Where this module fits

Module 03 produced **Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus**. This module extends that result by asking: **How can a multi-document contract remain understandable, relocatable, and deterministically buildable?**

The new capstone increment is **Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles**. It becomes the prerequisite for **Production HTTP API Design**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Resolve relative references from the correct document base.
- Use components where identity or reuse justifies them.
- Distinguish schema recursion from file-reference cycles.
- Bundle deterministically and work offline.
- Relocate the source tree without breaking resolution.

## Capstone increment

Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles.

## Core model

### Driving question

> How can a contract be modular without changing meaning or becoming a fragment maze?

### Observable outcome

Refactor the canonical contract into resolvable multi-document source, produce deterministic bundles, and prove the source survives relocation and offline execution.

### 1. A reference is URI resolution, not textual inclusion

`$ref: ../components/schemas/Project.yaml` identifies a target relative to the base URI of the document containing the reference. It does not paste text relative to the process working directory. Nested references acquire their own document base when resolution continues.

This matters when a source tree is bundled, moved, published, or loaded from a URL. A resolver that accidentally uses the shell directory can appear correct in one checkout and fail everywhere else.
### 2. Document identity and fragment identity are separate

The part before `#` selects a document; the fragment selects a location within it, commonly by JSON Pointer. `schemas.yaml#/Project` and `Project.yaml` are different organizational choices. `$id` can establish a base URI inside JSON Schema resources, and anchors can provide stable fragment names.

Use these features deliberately. Hidden base changes make references difficult to audit. The capstone prefers one schema per file and straightforward relative paths, reserving IDs and anchors for cases where they add actual portability.
### 3. Reference Objects and Schema `$ref` have context

OpenAPI Reference Objects can appear where the specification permits them. Inside a Schema Object, `$ref` follows JSON Schema semantics. Modern versions allow useful sibling behavior in schema contexts, but tool support and the exact referenced object type still matter.

Do not assume `$ref` means inheritance, merge, or macro expansion. Resolve the effective object according to the containing specification and verify the bundled result.
### 4. Splitting is an ownership decision

A good split gives a path group, schema, parameter, response, header, or security scheme one clear home. A bad split creates a file for every tiny field, hides local meaning behind long chains, or duplicates nearly identical schemas under different names.

The capstone groups path items by resource area and component files by component category. Extraction requires either reuse, independent review value, or a stable conceptual identity.
### 5. Bundling and dereferencing are different transformations

A bundle creates a self-contained description while usually preserving internal references. Dereferencing replaces references with target values and can explode recursive structures. Tools use the words inconsistently, so inspect output rather than inferring behavior from a command name.

The built-in course bundler resolves external references into one deterministic document and preserves no external path dependency. It emits a digest and compares operation ledgers before and after serialization.
### 6. Cycles can be legitimate or accidental

A recursive schema such as a tree node can intentionally reference itself. A cycle among files caused by organization can be accidental and unsupported by a generator. The correct question is whether the instance model is recursive, not whether the file graph contains a loop.

Document intentional recursion and include finite fixtures. Remove organizational cycles that add no domain meaning.
### 7. Relocation is the strongest simple reference test

Copy the source tree to a different absolute path, change the working directory, disconnect the network, and run resolution. If it fails, the source depends on undeclared context. The course’s reference gate resolves every target offline and treats remote dependency as a conscious publication decision.

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

1. Resolve `../components/schemas/Project.yaml` from `spec/paths/projects.yaml`.
2. Decode JSON Pointer `/components/schemas/A~1B~0C`.
3. When should a one-use schema stay inline?
4. Distinguish bundle and dereference.
5. Why can a recursive schema be valid while a generator fails?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For References and Multi-Document Architecture, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Relative references resolve against the base URI of the containing document. | URI/JSON Reference semantics | Working-directory resolution is incorrect. | offline reference gate and relocation exercise |
| JSON Pointer tokens escape `~` as `~0` and `/` as `~1`. | RFC 6901 semantics | Unescaped component names can point to the wrong location. | pointer unit cases |
| Every reusable object has one canonical definition. | course architecture policy | Duplicated schemas drift independently. | component inventory review |
| Bundling preserves the operation ledger and effective schemas. | course build invariant | Publication transformation must not change the contract. | bundle-check and example validation |
| The bundle is deterministic byte-for-byte for the same source. | course reproducibility policy | Hashes and release review require stable output. | SHA-256 evidence |
| All verifications run offline after setup. | course resilience policy | A contract should not depend on mutable remote fragments. | network-isolated reference test |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every References and Multi-Document Architecture claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the References and Multi-Document Architecture document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
# spec/openapi.yaml
paths:
  /projects:
    $ref: ./paths/projects.yaml
components:
  schemas:
    Project:
      $ref: ./components/schemas/Project.yaml
    ProjectCreate:
      $ref: ./components/schemas/ProjectCreate.yaml
  parameters:
    Limit:
      $ref: ./components/parameters/Limit.yaml

# spec/paths/projects.yaml
get:
  operationId: listProjects
  parameters:
    - $ref: ../components/parameters/Limit.yaml
  responses:
    '200':
      description: One project page
      content:
        application/json:
          schema:
            $ref: ../components/schemas/ProjectPage.yaml
```

### Close reading

- The reference in `openapi.yaml` starts from `spec/`; the nested references in `paths/projects.yaml` start from `spec/paths/`.
- Reusing `Limit` through both root components and a direct file reference can create duplicate identities; choose one convention and apply it consistently.
- Path Item files contain method fields directly because the root path key already supplies the target path.
- The publication bundle should contain the same methods and operation IDs even though file boundaries disappear.
- A reference target must be the correct object kind; a Schema Object cannot substitute for a Response Object merely because both are mappings.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Working-directory reference
- Wrong nested base
- Reference spaghetti
- Duplicate canonical schemas

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
def resolve_reference(reference: str, containing_document: Path) -> RefTarget:
    document_part, separator, fragment = reference.partition("#")
    target_document = (
        containing_document if not document_part
        else (containing_document.parent / document_part).resolve()
    )
    value = load_yaml(target_document)
    if separator:
        value = json_pointer_get(value, f"#{fragment}")
    return RefTarget(document=target_document, fragment=fragment, value=value)
```

### Why the code is shaped this way

- The containing document, not `Path.cwd()`, determines the target path.
- The resolver records target document and fragment so errors identify the full reference chain.
- A production-grade resolver also handles URI schemes, `$id`, anchors, dynamic references, caching, and cycle detection; the course engine intentionally scopes its claim.
- Tests include nested relative references and malformed JSON Pointers.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_bundle_is_relocatable_and_deterministic(tmp_path):
    source = Path("spec/openapi.yaml").resolve()
    first = bundle_document(source)
    second = bundle_document(source)

    canonical = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"))
    assert canonical(first) == canonical(second)
    assert operation_ledger(first) == operation_ledger(second)
    assert not validate_references(source)
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused References and Multi-Document Architecture check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
import assert from "node:assert/strict";
import { execFile as execFileCallback } from "node:child_process";
import { promisify } from "node:util";

const execFile = promisify(execFileCallback);
const source = "spec/openapi.yaml";
const output = "spec/dist/redocly.bundle.yaml";

await execFile("redocly", ["bundle", source, "--output", output]);
await execFile("spectral", ["lint", "--ruleset", ".spectral.yaml", source]);

// `load` and `operationLedger` are the focused helpers implemented in the lab.
assert.deepEqual(operationLedger(await load(source)), operationLedger(await load(output)));
```

### Why the code is shaped this way

- External tools are independent evidence, but the course also carries a readable resolver so learners can inspect the algorithm.
- Normalize semantically irrelevant key ordering before comparison; do not normalize away operation IDs, response codes, media types, or schemas.
- Run tools from a relocated checkout to catch implicit current-directory assumptions.
- Never edit `spec/dist/*`; regenerate it from source.

### Focused test excerpt

```typescript
it("preserves the operation ledger after bundling", async () => {
  const source = await loadYaml("spec/openapi.yaml");
  await execFile("redocly", ["bundle", "spec/openapi.yaml", "--output", "spec/dist/redocly.bundle.yaml"]);
  const bundled = await loadYaml("spec/dist/redocly.bundle.yaml");

  expect(operationLedger(bundled)).toEqual(operationLedger(source));
  expect(JSON.stringify(bundled)).not.toContain('"$ref":"./');
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For References and Multi-Document Architecture, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For References and Multi-Document Architecture, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Working-directory reference | Resolver joins relative paths to `cwd`. | Run the same command from another directory. | Resolve from the containing document URI. |
| Wrong nested base | A path file’s component reference is resolved from the root file. | Trace a two-hop reference and print each base. | Update base at each document boundary. |
| Reference spaghetti | A local operation requires opening many one-field files. | Count hops needed to understand one message. | Inline local details and extract only stable/reused concepts. |
| Duplicate canonical schemas | `Project` and `ProjectResponse` drift while describing the same public shape. | Diff effective bundled schemas. | Give one concept one canonical definition or intentionally separate direction-specific schemas. |
| Accidental cycle | Files refer to each other without recursive instance semantics. | Build a reference graph and find strongly connected components. | Remove organizational loops; retain only domain recursion. |
| Bundle changes meaning | Tool flattens or drops callbacks, examples, or siblings. | Compare operation ledger and targeted effective objects. | Pin tool, preserve source, and fail capability/report checks. |
| Remote mutable reference | Build downloads `main/openapi.yaml` from another repository. | Run offline or after upstream changes. | Vendor immutable artifacts or pin content-addressed versions. |

### Defect-injection protocol

Use the module lab to inject the named references and multi-document architecture defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Refactor the canonical contract into resolvable multi-document source, produce deterministic bundles, and prove the source survives relocation and offline execution.

This References and Multi-Document Architecture increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/openapi.yaml`
- `capstone/spec/paths/`
- `capstone/spec/components/`
- `capstone/spec/dist/`
- `capstone/scripts/spec_tools.py`
- `capstone/scripts/course_tool.py`
- `capstone/redocly.yaml`
- `capstone/.spectral.yaml`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- offline multi-document source
- deterministic bundles and checksums
- reference-resolution report
- component extraction review

### Commit boundary

The References and Multi-Document Architecture checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Resolve relative references from the correct document base, Use components where identity or reuse justifies them, and Distinguish schema recursion from file-reference cycles** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Repair the path and remove one needless reference hop found during review** and requiring the following oracle: **all references resolve offline; nested references use the correct document base; two bundles are deterministic; source and bundle operation ledgers match.**

The cumulative platform now includes **Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Production HTTP API Design](../module-05-production-http-api-design/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
