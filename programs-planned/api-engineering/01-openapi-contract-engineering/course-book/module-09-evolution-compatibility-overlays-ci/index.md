# Module 09 — Evolution, Compatibility, and Audience Views

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** How can a published API evolve without silently breaking request writers or response readers?

## Where this module fits

Module 08 produced **Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures**. This module extends that result by asking: **How can a published API evolve without silently breaking request writers or response readers?**

The new capstone increment is **Create compatible and rejected release candidates, compatibility gates, and public/partner audience views**. It becomes the prerequisite for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Analyze compatibility in the correct message direction.
- Treat requiredness, enums, media types, statuses, and operation IDs as consumer commitments.
- Design deprecation and major-version migration.
- Apply Overlay documents deterministically.
- Block incompatible minor releases in CI.

## Capstone increment

Create compatible and rejected release candidates, compatibility gates, and public/partner audience views.

## Core model

### Driving question

> How can a published contract change without silently invalidating consumer assumptions?

### Observable outcome

Classify request- and response-side compatibility, archive reproducible releases, block an intentionally breaking minor change, produce approved major migration evidence, and derive public/partner views through Overlay documents.

### 1. Compatibility is directional

A provider receives requests and emits responses; a consumer emits requests and receives responses. Widening what the provider accepts is usually request-compatible, while widening what it emits can break strict consumers. Making a request field optional may help new callers but can conflict with old providers if a consumer starts omitting it.

Every change review therefore names the direction and the compared actors: new provider with old consumer, old provider with new consumer, or generated source compatibility. “Non-breaking” without a direction is incomplete.
### 2. Schema widening and narrowing reverse across the boundary

For request schemas, loosening a maximum or adding an accepted enum value generally widens provider acceptance. For response schemas, emitting values outside the old contract widens provider output and may break old consumers. Adding a required response property is often wire-compatible for tolerant consumers but can break exact decoders, generated constructors, signatures, or snapshots.

Compatibility tools apply documented heuristics, not universal truth. The course combines automated diff classification with scenario-specific review notes for enums, unions, `additionalProperties`, numeric precision, and generated client behavior.
### 3. Operation identity is part of source compatibility

Changing an `operationId` does not alter HTTP routing, yet generated client methods, Arazzo references, links, tests, and documentation anchors may break. Treat it as a consumer-facing rename. A compatibility gate should report it even if a pure wire diff might not.

The attempted v1.2 fixture changes one operation ID deliberately. The release gate identifies the exact old/new values and blocks the minor release.
### 4. Additive changes still carry risk

A new optional request field is often safe. A new response field can break clients that reject unknown properties. A new enum response member can break exhaustive switches. A new success status may bypass code expecting one exact branch. A new optional security alternative may weaken policy if misunderstood.

“Additive” is a syntactic description, not a compatibility verdict. Release review states consumer assumptions and tests representative generated clients where risk is material.
### 5. Deprecation is a lifecycle, not a Boolean flag

`deprecated: true` communicates intent but does not identify replacement, timeline, telemetry, or removal conditions. A useful deprecation plan names affected operations or fields, replacement path, first deprecated release, support window, migration examples, and planned major version.

The contract, changelog, documentation, and runtime headers should tell one story. Removal occurs only in a release whose compatibility policy permits it.
### 6. Versioning should follow the actual compatibility boundary

URI versions create explicit parallel resources but can duplicate surface area. Header or media-type versions keep URIs stable but complicate discovery, caching, and tooling. Semantic artifact versions communicate release intent but do not select runtime behavior alone.

The capstone archives versioned contract artifacts and treats incompatible removal as v2.0. It does not implement multiple runtime routers merely to demonstrate version syntax. The migration document is more important than decorative `/v1` prefixes.
### 7. Release artifacts must be immutable and reproducible

A release directory contains the exact bundled contract, checksum, changelog, compatibility report, generator/tool versions, and migration evidence where required. Rebuilding from the tagged source must reproduce the digest. Editing a historical contract in place destroys auditability.

The main branch can keep modular sources; consumers receive an immutable bundle. CI compares the candidate bundle to the selected released baseline, not to an arbitrary previous commit.
### 8. Automated diffing is a gate with human review boundaries

Diff tools efficiently identify removed operations, changed requiredness, narrower constraints, security changes, and response differences. They can miss domain invariants, generated-source breakage, and client strictness. They may also classify harmless documentation edits.

The course stores both machine report and reviewer decision. Suppression requires an exact rule, rationale, affected consumers, and expiration or release scope. A clean diff is evidence, not proof that no consumer can break.
### 9. Overlays derive views without copying the source

An Overlay document applies ordered actions to a target OpenAPI description using JSONPath selection. It can update servers or descriptions and remove internal paths for a public or partner view. The target remains canonical; the overlay records the transformation intent.

Order matters. Removing a subtree before trying to update it changes the result. Broad JSONPath selectors can unintentionally touch new operations added later, so transformed artifacts require forbidden-path and expected-operation assertions.
### 10. CI should fail with actionable compatibility evidence

A useful gate names the baseline and candidate digests, exact paths/pointers, change classification, policy outcome, and remediation. “Breaking changes found” without locations wastes review time. The attempted minor fixture includes three independent defects so the report must find all three rather than stop at the first.

A major release may permit intentional breaks only when an explicit approval marker and migration document exist. This prevents version-number inflation from bypassing review.

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

1. Why can adding a response enum value be breaking?
2. Is removing a maximum from a request string compatible?
3. Is adding a required response property breaking?
4. Why is changing operationId risky without wire change?
5. What belongs in a deprecation record?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Compatibility, Releases, Overlay, and CI, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Compatibility reviews state request/response direction and old/new actor assumptions. | review policy | A change can be safe in one direction and unsafe in another. | change-case matrix |
| OperationId changes are treated as consumer-facing compatibility changes. | course policy | Generated code, links, and workflows reference them. | attempted v1.2 fixture |
| Historical release artifacts and checksums are immutable. | release policy | Audit and reproducible generation require exact baselines. | release directories and digest report |
| A minor release with a detected breaking change is blocked. | semantic release policy | Consumers should not discover incompatible changes by regeneration or production failure. | compatibility gate |
| A breaking major release requires explicit migration evidence and approval. | governance-light release rule | A major number alone does not help consumers migrate. | v2.0 fixture and migration document |
| Overlay outputs are validated for expected operations and forbidden internal content. | transformation policy | Correct syntax does not guarantee a safe derived audience view. | overlay assertions |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Compatibility, Releases, Overlay, and CI claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Compatibility, Releases, Overlay, and CI document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
overlay: 1.1.0
info:
  title: Public Analysis Runs API view
  version: 1.0.0
actions:
  - target: $.info
    update:
      description: Public contract for submitting and observing analysis work.
  - target: $.servers
    update:
      - url: https://api.example.test
        description: Public production endpoint
  - target: $.paths['/internal/diagnostics']
    remove: true
  - target: $.tags[?(@.name == 'Internal')]
    remove: true
```

### Close reading

- Actions are applied in document order; later targets see the result of earlier actions.
- JSONPath selects target nodes while `update` and `remove` define the transformation.
- The overlay is a companion artifact, not a second manually maintained OpenAPI source.
- After transformation, tests assert the diagnostics path and Internal tag are absent and all required public operation IDs remain.
- Tool support for Overlay actions is recorded; the course includes a bounded local implementation for proof portability.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- All additions called safe
- Wrong baseline
- Historical contract edited
- OperationId dismissed as metadata

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
def classify_operation_changes(old: dict, new: dict) -> list[Change]:
    changes: list[Change] = []
    old_ops = operation_map(old)
    new_ops = operation_map(new)
    for key, old_operation in old_ops.items():
        if key not in new_ops:
            changes.append(Change("breaking", key, "operation removed"))
            continue
        new_operation = new_ops[key]
        if old_operation["operationId"] != new_operation["operationId"]:
            changes.append(Change("breaking", key, "operationId changed"))
        removed_responses = set(old_operation["responses"]) - set(new_operation["responses"])
        for status in sorted(removed_responses):
            changes.append(Change("breaking", key, f"response {status} removed"))
    return changes
```

### Why the code is shaped this way

- The local comparator intentionally covers a documented subset and is paired with oasdiff when available.
- Classify exact method/path identity first, then parameters, schemas, responses, and security in deeper passes.
- Write reports in deterministic order and include contract digests so CI evidence can be reproduced.
- Never label an unimplemented comparison category as safe; label it unassessed and require another route.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_minor_release_gate_detects_every_planted_break():
    old = load_yaml(Path("releases/v1.1/openapi.yaml"))
    attempted = load_yaml(Path("releases/attempted-v1.2-breaking/openapi.yaml"))
    report = compare_contracts(old, attempted)

    assert report["compatible"] is False
    messages = "\n".join(change["reason"] for change in report["breaking"])
    assert "operationId" in messages
    assert "response" in messages
    assert "pattern" in messages
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Evolution, Compatibility, and Audience Views check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
const report = await run("oasdiff", [
  "breaking",
  "releases/v1.1/openapi.yaml",
  "releases/attempted-v1.2-breaking/openapi.yaml",
  "--format", "json",
]);

if (report.exitCode === 0) {
  throw new Error("fixture error: the intentionally breaking candidate was not blocked");
}
const parsed = JSON.parse(report.stdout);
assertReported(parsed, [
  "operationId changed",
  "response removed",
  "pattern became more restrictive",
]);
```

### Why the code is shaped this way

- Testing the gate with an intentionally bad fixture prevents a misconfigured diff command from returning false green.
- The wrapper preserves stdout/stderr and tool version in a report rather than reducing the result to an exit code.
- Exact output structure varies by pinned tool version, so adapters normalize categories without deleting source detail.
- The built-in comparator remains available when the external binary is absent, but capability status must say which ran.

### Focused test excerpt

```typescript
it("rejects the deliberately breaking minor candidate", async () => {
  const report = await run("oasdiff", [
    "breaking",
    "releases/v1.1/openapi.yaml",
    "releases/attempted-v1.2-breaking/openapi.yaml",
    "--format", "json",
  ]);

  expect(report.exitCode).not.toBe(0);
  expect(report.combinedOutput).toContain("operationId");
  expect(report.combinedOutput).toContain("response");
  expect(report.combinedOutput).toContain("pattern");
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Compatibility, Releases, Overlay, and CI, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Compatibility, Releases, Overlay, and CI, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| All additions called safe | New enum/status/field breaks a strict consumer. | Regenerate or run an exhaustive consumer fixture. | Review direction and representative client assumptions. |
| Wrong baseline | Candidate is compared to an arbitrary commit. | Inspect CI inputs on a branch. | Select immutable latest supported release artifact and digest. |
| Historical contract edited | Old checksum changes after documentation repair. | Recompute release digest. | Never mutate releases; issue a new artifact/version. |
| OperationId dismissed as metadata | Generated method disappears or changes name. | Regenerate client after rename. | Treat stable operation identity as compatibility surface. |
| Deprecation without migration | Flag remains for years or removal surprises users. | Search for replacement/timeline evidence. | Publish lifecycle, telemetry, support window, and examples. |
| Overlay selector too broad | New internal or public operation is changed unexpectedly. | Add a matching path/tag and reapply. | Use precise selectors and assert expected/forbidden output. |
| Major version bypass | Breaking release passes because version starts with 2. | Remove migration/approval and rerun. | Require evidence independent of version string. |
| Diff tool treated as oracle | Domain or generator break is missed. | Exercise a strict consumer or state invariant. | Combine automated diff, client regeneration, and contextual review. |

### Defect-injection protocol

Use the module lab to inject the named evolution, compatibility, and audience views defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Classify request- and response-side compatibility, archive reproducible releases, block an intentionally breaking minor change, produce approved major migration evidence, and derive public/partner views through Overlay documents.

This Compatibility, Releases, Overlay, and CI increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/releases/v1.0/`
- `capstone/releases/v1.1/`
- `capstone/releases/attempted-v1.2-breaking/`
- `capstone/releases/v2.0/`
- `capstone/spec/overlays/public.overlay.yaml`
- `capstone/spec/overlays/partner.overlay.yaml`
- `capstone/tests/compatibility/change-cases.yaml`
- `capstone/docs/compatibility.md`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- immutable v1.0/v1.1/v2.0 artifacts
- blocked minor-change fixture
- migration evidence
- verified public and partner views

### Commit boundary

The Compatibility, Releases, Overlay, and CI checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Analyze compatibility in the correct message direction, Treat requiredness, enums, media types, statuses, and operation IDs as consumer commitments, and Design deprecation and major-version migration** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **v1.1 is classified non-breaking under stated policy; attempted v1.2 fails for all planted defects; v2.0 needs migration and approval evidence; release bundles reproduce exact digests.**

The cumulative platform now includes **Create compatible and rejected release candidates, compatibility gates, and public/partner audience views**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [OpenAPI 3.2, Streaming, Webhooks, and Workflows](../module-10-openapi-32-workflows-advanced/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
