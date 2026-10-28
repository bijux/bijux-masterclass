# Worked Answers — Module 08: Security in the Public Contract

Use these solutions to audit your reasoning for **Security in the Public Contract**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Translate `security: [{ bearerAuth: [], mtls: [] }, { apiKeyAuth: [] }]`.

The caller must provide bearer AND mutual TLS, OR provide the API key alternative.

The chapter’s decisive distinction is this: An OpenAPI Security Scheme tells a consumer where credentials travel and which protocol vocabulary applies: an API key in a header, HTTP bearer authentication, OAuth flows, OpenID Connect discovery, or mutual TLS. It does not validate a signature, issue a token, rotate a key, or decide whether a principal may read one artifact.

## 2. What does `security: []` mean on an operation?

It explicitly replaces inherited requirements with an anonymous alternative.

In the cumulative capstone, the rule becomes concrete: A root-level requirement reduces repetition but creates hidden inheritance. An operation with no security field inherits it. security: [] explicitly allows anonymous access. An operation-level non-empty array replaces the root requirement rather than adding to it.

**Counterexample.** Root-level security is still inherited because the operation override was omitted or misread.

**Evidence.** Resolve root inheritance and call the operation anonymously and with credentials, confirming that only this operation is anonymous.

## 3. Why is an OAuth2 scheme not an OAuth server?

It describes flows, token endpoint metadata, and scopes for consumers; it does not issue or verify tokens at runtime.

A useful way to reason about the boundary is: The capstone deliberately uses deterministic local credentials so the contract and authorization paths can be tested without pretending to implement a production identity provider. The limitation is explicit: token issuance, cryptographic verification, revocation, and key management belong to an external security system.

## 4. When is 404 preferable to 403?

When policy intentionally conceals whether a resource exists across an authorization boundary and the behavior is applied consistently.

The implementation consequence is: Use 401 Unauthorized when authentication is absent or invalid and include an appropriate challenge when the HTTP scheme requires it. Use 403 Forbidden when the principal is authenticated but lacks permission and revealing the resource or policy is acceptable. Use 404 Not Found deliberately when resource existence must not be disclosed across ownership boundaries.

## 5. Why must scope and owner tests be separate?

A principal can have the correct coarse permission but lack relationship permission to one object; combining cases can leave this gap untested.

The important nuance is: Authentication establishes a principal. Scope authorization asks whether that principal holds a coarse permission such as runs:write. Ownership or relationship authorization asks whether this principal may act on this specific project, dataset, run, artifact, or webhook subscription.

**Evidence.** Run a Cartesian matrix of scope and ownership, including correct-scope/wrong-owner and wrong-scope/correct-owner cases.

## 6. Design a minimum-scope test for `createAnalysisRun`.

Use no credential, invalid credential, read-only token, write token, and another owner’s dataset. Assert 401, 401, 403, success for owned dataset, and concealed rejection for foreign dataset.

Under concurrency or failure, the distinction becomes: Every operation maps to the minimum scope needed for its observable action. Read and write permissions are separated. An operation that only accepts anonymous health checks uses no scope. The matrix is reviewed with the contract and executed against credential fixtures.

## 7. Why is `format: uri` insufficient for webhook safety?

It does not block private networks, dangerous schemes, DNS rebinding, redirects, credentials in URLs, or egress-policy violations.

The design remains honest only if: Accepting an arbitrary callback URL can turn a provider into an SSRF primitive that reaches loopback, metadata services, private networks, or unsupported protocols. A schema format: uri checks syntax at best; it does not establish network safety.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 8. What should a 401 bearer response normally include?

A `WWW-Authenticate` challenge appropriate to the scheme, without leaking secret validation internals.

The consumer-facing consequence is: Documentation, mock examples, generated tests, reports, and CI logs are durable replication surfaces. A real key placed in an OpenAPI example may be copied into static sites and caches. Use conspicuously synthetic credentials and automatic secret scanning.

**Counterexample.** The provider returns a generic problem without the protocol challenge needed by a bearer client.

**Evidence.** Assert the WWW-Authenticate challenge, stable problem body, and absence of token-validation internals for missing and invalid bearer credentials.

## 9. How does `additionalProperties: false` help security?

It rejects undeclared fields and reduces over-posting, but it does not sanitize values for contextual sinks.

The operational consequence is: Length limits, enum constraints, media-type restrictions, and additionalProperties: false reduce accidental and malicious payload space. They do not make strings safe for SQL, shells, URLs, file paths, or logs. Security depends on contextual handling after schema validation.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 10. Name evidence that the contract and runtime security agree.

An operation-security matrix derived from the contract, live tests across identity fixtures, matching statuses/challenges/problems, ownership cases, and a report tied to the contract digest.

The strongest engineering interpretation is: This Security Contracts and Runtime Enforcement increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

**Evidence.** Resolve the effective security requirement per operation and run missing, invalid, insufficient, foreign-owner, and successful credential scenarios against both providers.

## 11. Practical defect exercise

For **Declaration without enforcement**, a valid solution must first reproduce: the description declares a scope but the runtime ignores it. The smallest useful starting case is: call a write operation with a read-only token. The repair is: execute matrix-based live authorization tests.

The defect-oriented view is: For Security Contracts and Runtime Enforcement, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

## 12. Cross-language parity exercise

The Security Contracts and Runtime Enforcement parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: For every Security Contracts and Runtime Enforcement claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.
