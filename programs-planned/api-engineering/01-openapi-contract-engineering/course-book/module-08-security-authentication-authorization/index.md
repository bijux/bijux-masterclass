# Module 08 — Security in the Public Contract

> **Program stage:** Course 1 of 10 — Specify the public promise.

> **Central question:** What can the public contract say about authentication and authorization, and what remains a runtime responsibility?

## Where this module fits

Module 07 produced **Build the consumer and contract-test ladder against the mock and both real providers**. This module extends that result by asking: **What can the public contract say about authentication and authorization, and what remains a runtime responsibility?**

The new capstone increment is **Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures**. It becomes the prerequisite for **Evolution, Compatibility, and Audience Views**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Model API-key and bearer security schemes.
- Read AND/OR semantics in security requirements correctly.
- Use global security and operation overrides deliberately.
- Separate authentication, authorization, and ownership.
- Document security failures without leaking implementation details.

## Capstone increment

Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures.

## Core model

### Driving question

> How do security declarations, credentials, scopes, ownership, and runtime enforcement fit together?

### Observable outcome

Model API-key and OAuth-style requirements correctly, implement deterministic authentication and scope/ownership enforcement in both providers, and prove every public operation has an explicit security decision.

### 1. A Security Scheme describes credential transport, not trust

An OpenAPI Security Scheme tells a consumer where credentials travel and which protocol vocabulary applies: an API key in a header, HTTP bearer authentication, OAuth flows, OpenID Connect discovery, or mutual TLS. It does not validate a signature, issue a token, rotate a key, or decide whether a principal may read one artifact.

The capstone deliberately uses deterministic local credentials so the contract and authorization paths can be tested without pretending to implement a production identity provider. The limitation is explicit: token issuance, cryptographic verification, revocation, and key management belong to an external security system.
### 2. Security Requirement Objects express alternatives and combinations

Each object in the security array is an alternative—logical OR. Multiple scheme names inside one object are required together—logical AND. `security: [{ bearerAuth: [] }, { apiKeyAuth: [] }]` means bearer OR API key. `security: [{ bearerAuth: [], clientCertificate: [] }]` means both.

Misreading this structure can make an operation impossible to call or weaker than intended. Exercises translate every declaration into plain Boolean logic before implementation.
### 3. Global security is inherited unless explicitly overridden

A root-level requirement reduces repetition but creates hidden inheritance. An operation with no `security` field inherits it. `security: []` explicitly allows anonymous access. An operation-level non-empty array replaces the root requirement rather than adding to it.

The capstone uses global bearer-or-API-key authentication and explicit anonymous health. Diagnostics overrides the root with an administrator scope. A mechanical matrix checks that no operation’s security decision is merely accidental omission.
### 4. Authentication, scope authorization, and ownership are separate gates

Authentication establishes a principal. Scope authorization asks whether that principal holds a coarse permission such as `runs:write`. Ownership or relationship authorization asks whether this principal may act on this specific project, dataset, run, artifact, or webhook subscription.

A token with `artifacts:read` is not permission to retrieve every tenant’s artifact. The capstone centralizes resource lookup through owner-aware store methods, then tests correct scope/wrong owner independently from missing scope.
### 5. 401, 403, and concealed 404 communicate different boundaries

Use `401 Unauthorized` when authentication is absent or invalid and include an appropriate challenge when the HTTP scheme requires it. Use `403 Forbidden` when the principal is authenticated but lacks permission and revealing the resource or policy is acceptable. Use `404 Not Found` deliberately when resource existence must not be disclosed across ownership boundaries.

Consistency matters more than a slogan. The security model documents which object-level checks conceal existence, and both providers follow the same table. Never return different timing or detail text that defeats the concealment policy.
### 6. Scopes are an interface vocabulary, not a full policy language

Scopes should be stable, comprehensible consumer permissions such as `projects:read` and `runs:write`. They should not encode dynamic resource IDs, employee titles, or internal database roles. Fine-grained policy remains runtime logic.

Every operation maps to the minimum scope needed for its observable action. Read and write permissions are separated. An operation that only accepts anonymous health checks uses no scope. The matrix is reviewed with the contract and executed against credential fixtures.
### 7. Input constraints reduce attack surface but do not sanitize intent

Length limits, enum constraints, media-type restrictions, and `additionalProperties: false` reduce accidental and malicious payload space. They do not make strings safe for SQL, shells, URLs, file paths, or logs. Security depends on contextual handling after schema validation.

The capstone constrains names, identifiers, upload size, and webhook URLs. It still avoids shell interpolation, treats uploaded bytes as opaque, escapes logs, and validates outbound destinations before any callback delivery.
### 8. Webhook and callback URLs create outbound trust problems

Accepting an arbitrary callback URL can turn a provider into an SSRF primitive that reaches loopback, metadata services, private networks, or unsupported protocols. A schema `format: uri` checks syntax at best; it does not establish network safety.

The training provider restricts subscriptions to `https`, rejects userinfo and loopback/private host forms, and does not actually deliver over the network. A production design would also resolve and re-check DNS, restrict redirects, enforce egress policy, sign messages, retry safely, and manage secrets.
### 9. Secrets must not appear in contract examples or evidence

Documentation, mock examples, generated tests, reports, and CI logs are durable replication surfaces. A real key placed in an OpenAPI example may be copied into static sites and caches. Use conspicuously synthetic credentials and automatic secret scanning.

Even deterministic training tokens are treated as public fixtures, not secrets. Reports redact Authorization and API-key fields so the evidence mechanism is safe when adapted to real environments.
### 10. Security drift is observable behavior

A contract may declare a scope while a provider forgets to enforce it; a provider may require authentication on an operation declared anonymous; or Python and TypeScript may conceal ownership differently. Static review cannot resolve these cases.

The shared security suite iterates the operation-scope matrix with anonymous, invalid, read-only, write, other-owner, API-key, and administrator identities. It asserts status, challenge where applicable, problem media type, and resource non-disclosure.

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

1. Translate `security: [{ bearerAuth: [], mtls: [] }, { apiKeyAuth: [] }]`.
2. What does `security: []` mean on an operation?
3. Why is an OAuth2 scheme not an OAuth server?
4. When is 404 preferable to 403?
5. Why must scope and owner tests be separate?

A weak answer repeats a keyword. A complete answer predicts an observable request, response, or consumer failure.

## Standards and contract rules

### Read standards with category discipline

For Security Contracts and Runtime Enforcement, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

| Claim | Category | Why it matters | Evidence |
|---|---|---|---|
| Every path operation has an explicit effective security decision recorded in the scope matrix. | course security rule | Implicit inheritance must still be reviewed and testable. | security matrix audit |
| Security array elements are OR alternatives; scheme names within one element are AND requirements. | OAS semantics | Incorrect Boolean interpretation changes who can call an operation. | truth-table exercises |
| A valid security declaration is not evidence of runtime enforcement. | verification limit | OpenAPI is descriptive and cannot authenticate or authorize. | live security suite |
| Scope checks and object ownership checks are tested independently. | authorization policy | A broad scope must not cross tenant/resource boundaries. | other-owner artifact scenario |
| Validation, logs, examples, and reports never contain production secrets. | operational security policy | Documentation and CI artifacts are replication surfaces. | secret fixture and redaction review |
| User-supplied webhook destinations are constrained beyond URI syntax before use. | outbound security policy | Syntactically valid URLs can target sensitive networks. | webhook validation tests |

### Four labels used in review

**Normative requirement.** The cited specification defines required behavior or document structure.

**Interoperability recommendation.** Multiple legal choices exist, but one choice reduces ambiguity across providers or tools.

**Course policy.** The capstone chooses a stricter invariant so completion can be tested mechanically.

### Normative review exercise

For every Security Contracts and Runtime Enforcement claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—`parse`, `examples`, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

### Exit test

Explain how the Security Contracts and Runtime Enforcement document could satisfy every structural row while a provider still violates the public boundary. Identify the highest-risk claim here that YAML alone cannot establish.

## Worked contract design

### Starting fragment

```yaml
security:
  - bearerAuth: []
  - apiKeyAuth: []

paths:
  /health:
    get:
      operationId: getHealth
      security: []
      responses:
        '200':
          $ref: ./components/responses/Health.yaml
  /internal/diagnostics:
    get:
      operationId: getDiagnostics
      security:
        - bearerAuth: [admin:read]
      responses:
        '200':
          description: Diagnostic summary
        '401':
          $ref: ./components/responses/Unauthorized.yaml
        '403':
          $ref: ./components/responses/Forbidden.yaml

components:
  securitySchemes:
    bearerAuth:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://identity.example.test/oauth/token
          scopes:
            admin:read: Read internal diagnostics
    apiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### Close reading

- The two root array elements mean bearer OR API key, not both.
- `security: []` on health replaces inherited requirements with anonymous access.
- Diagnostics replaces the root alternatives with bearer plus the administrator scope.
- The token URL documents the flow but the training service does not implement token issuance.
- Runtime tests still need to prove 401, 403, and successful paths for each declared alternative.

Do not begin by rendering the document. Inspect it in this order:

Plant each of these defect classes one at a time and predict which gate should fail first:

- Declaration without enforcement
- OR interpreted as AND
- Scope treated as ownership
- Anonymous override omitted

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
def require(scopes: set[str]):
    async def dependency(
        authorization: str | None = Header(default=None),
        api_key: str | None = Header(default=None, alias="X-API-Key"),
    ) -> Principal:
        principal = authenticate(authorization=authorization, api_key=api_key)
        missing = scopes - principal.scopes
        if missing:
            raise ApiProblem.forbidden(code="insufficient-scope", missing=sorted(missing))
        return principal
    return dependency

@app.get("/artifacts/{artifact_id}", response_model=Artifact, operation_id="getArtifact")
async def get_artifact(
    artifact_id: str,
    principal: Principal = Depends(require({"artifacts:read"})),
) -> Artifact:
    return store.get_owned_artifact(principal.subject, artifact_id)
```

### Why the code is shaped this way

- Authentication accepts exactly the alternatives documented by the contract; malformed combinations have deterministic behavior.
- The scope dependency handles coarse permission, while `get_owned_artifact` applies object-level concealment.
- Public `ApiProblem` creation is centralized so challenge/header and media type remain consistent.
- Do not put production token parsing or signature verification in a tutorial shortcut and call it secure.

### Focused test excerpt

The fixtures and helpers are defined in `capstone/services/python-fastapi/tests/`. This excerpt is intentionally executable rather than pseudocode.

```python
def test_scope_and_ownership_are_independent(client, write_headers, read_headers):
    created = client.post("/projects", headers=write_headers, json={"name": "Owned"})
    project_id = created.json()["id"]

    denied_write = client.post("/projects", headers=read_headers, json={"name": "Denied"})
    concealed_read = client.get(
        f"/projects/{project_id}",
        headers={"Authorization": "Bearer other-owner"},
    )

    assert denied_write.status_code == 403
    assert concealed_read.status_code == 404
    assert concealed_read.json()["type"].endswith("/not-found")
```

The complete test suite adds the complementary failure branches and shared live scenario.

### Completion evidence

Begin with the focused Security in the Public Contract check, then run the provider-neutral route so one implementation cannot hide public drift.

## TypeScript implementation

### Boundary implementation

```typescript
export function requireScopes(required: readonly Scope[]) {
  return async function guard(request: FastifyRequest): Promise<void> {
    const principal = authenticate(request.headers.authorization, request.headers["x-api-key"]);
    const missing = required.filter((scope) => !principal.scopes.has(scope));
    if (missing.length > 0) {
      throw ApiProblem.forbidden("insufficient-scope", { missing });
    }
    request.principal = principal;
  };
}

app.get("/artifacts/:artifactId", {
  preHandler: requireScopes(["artifacts:read"]),
  schema: artifactRouteSchema,
}, async (request) => store.getOwnedArtifact(request.principal.subject, request.params.artifactId));
```

### Why the code is shaped this way

- The request principal is populated only after successful authentication and typed through module augmentation.
- Route response schemas filter internal fields and document the public problem branches.
- Owner-aware store methods avoid a dangerous pattern of fetching globally and checking ownership inconsistently in handlers.
- The same credential fixtures and scope matrix drive Fastify and FastAPI live tests.

### Focused test excerpt

```typescript
it("does not let broad scope cross an ownership boundary", async () => {
  const created = await app.inject({
    method: "POST", url: "/projects", headers: writeHeaders, payload: { name: "Owned" },
  });
  const projectId = created.json<{ id: string }>().id;

  const deniedWrite = await app.inject({
    method: "POST", url: "/projects", headers: { authorization: "Bearer learner-read" }, payload: { name: "Denied" },
  });
  const concealedRead = await app.inject({
    method: "GET", url: `/projects/${projectId}`, headers: { authorization: "Bearer other-owner" },
  });

  expect(deniedWrite.statusCode).toBe(403);
  expect(concealedRead.statusCode).toBe(404);
});
```

The provider-neutral live suite repeats the semantic assertion through an actual base URL.

### Completion evidence

For Security Contracts and Runtime Enforcement, type-checking proves source consistency, Vitest proves selected runtime behavior, and shared live conformance proves provider parity. Report those as separate evidence claims.

## Failure patterns

For Security Contracts and Runtime Enforcement, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

| Failure | Observable symptom | Smallest reproducer | Repair |
|---|---|---|---|
| Declaration without enforcement | Docs show a scope but runtime ignores it. | Call write operation with read-only token. | Execute matrix-based live authorization tests. |
| OR interpreted as AND | Clients are required to send bearer and API key together. | Try each documented alternative independently. | Translate Security Requirement arrays into Boolean logic and test each branch. |
| Scope treated as ownership | Correct scope reads another user’s artifact. | Use `other-owner` resource ID with learner token. | Apply owner-aware lookup after scope authorization. |
| Anonymous override omitted | Health unexpectedly requires credentials. | Call health without headers. | Use explicit `security: []` and matrix audit. |
| Existence leak | Wrong owner receives a different detail/status than missing ID. | Compare both requests and timing envelope. | Apply documented concealed 404 behavior consistently. |
| URI format trusted for callbacks | Loopback or metadata URL is accepted. | Submit `https://127.0.0.1/...` and encoded/private variants. | Constrain scheme/host and enforce outbound network policy before delivery. |
| Secret in example | A real-looking credential enters docs and logs. | Search built artifacts and reports. | Use synthetic fixtures, redaction, and secret scanning. |
| Over-posting | Client sets owner or server status in input. | Send undeclared server-owned fields. | Use separate closed input schemas and response serializers. |

### Defect-injection protocol

Use the module lab to inject the named security in the public contract defect. Predict its first failing oracle before changing the implementation.

### Diagnostic discipline

Classify the failure before editing and start at the lowest evidence layer capable of falsifying the claim.

## What you add to the capstone

### Increment promise

Model API-key and OAuth-style requirements correctly, implement deterministic authentication and scope/ownership enforcement in both providers, and prove every public operation has an explicit security decision.

This Security Contracts and Runtime Enforcement increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

### Primary working set

- `capstone/spec/components/security-schemes/`
- `capstone/tests/security/scope-matrix.yaml`
- `capstone/services/python-fastapi/src/analysis_api/auth.py`
- `capstone/services/typescript-fastify/src/auth.ts`
- `capstone/spec/paths/webhook-subscriptions.yaml`
- `capstone/docs/security-model.md`

The paths identify the main review surface, not permission to ignore related references, fixtures, or documentation.

### Required deliverables

- effective security matrix
- scope and ownership enforcement
- webhook destination constraints
- security live report

### Commit boundary

The Security Contracts and Runtime Enforcement checkpoint commit should contain only this coherent vertical slice and its evidence. Remove temporary planted defects while preserving their minimized reproducers and permanent regressions.

## Module synthesis

You are ready to leave this module when you can **Model API-key and bearer security schemes, Read AND/OR semantics in security requirements correctly, and Use global security and operation overrides deliberately** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Translate all security failures to documented Problem Details and add required challenge headers** and requiring the following oracle: **health is explicitly anonymous; each documented credential alternative works independently; missing/invalid/insufficient credentials are distinct; scope does not bypass ownership.**

The cumulative platform now includes **Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Evolution, Compatibility, and Audience Views](../module-09-evolution-compatibility-overlays-ci/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
