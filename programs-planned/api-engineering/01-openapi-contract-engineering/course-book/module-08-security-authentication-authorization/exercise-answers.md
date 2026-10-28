# Reference Answers — Module 08: Security in the Public Contract

Read after attempting all twelve Security in the Public Contract exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Translate `security: [{ bearerAuth: [], mtls: [] }, { apiKeyAuth: [] }]`.

The caller must provide bearer AND mutual TLS, OR provide the API key alternative.

## 2. What does `security: []` mean on an operation?

It explicitly replaces inherited requirements with an anonymous alternative.

## 3. Why is an OAuth2 scheme not an OAuth server?

It describes flows, token endpoint metadata, and scopes for consumers; it does not issue or verify tokens at runtime.

## 4. When is 404 preferable to 403?

When policy intentionally conceals whether a resource exists across an authorization boundary and the behavior is applied consistently.

## 5. Why must scope and owner tests be separate?

A principal can have the correct coarse permission but lack relationship permission to one object; combining cases can leave this gap untested.

## 6. Design a minimum-scope test for `createAnalysisRun`.

Use no credential, invalid credential, read-only token, write token, and another owner’s dataset. Assert 401, 401, 403, success for owned dataset, and concealed rejection for foreign dataset.

## 7. Why is `format: uri` insufficient for webhook safety?

It does not block private networks, dangerous schemes, DNS rebinding, redirects, credentials in URLs, or egress-policy violations.

## 8. What should a 401 bearer response normally include?

A `WWW-Authenticate` challenge appropriate to the scheme, without leaking secret validation internals.

## 9. How does `additionalProperties: false` help security?

It rejects undeclared fields and reduces over-posting, but it does not sanitize values for contextual sinks.

## 10. Name evidence that the contract and runtime security agree.

An operation-security matrix derived from the contract, live tests across identity fixtures, matching statuses/challenges/problems, ownership cases, and a report tied to the contract digest.

## 11. Practical defect exercise

For **Declaration without enforcement**, a valid solution must first reproduce: the description declares a scope but the runtime ignores it. The smallest useful starting case is: call a write operation with a read-only token. The repair is: execute matrix-based live authorization tests.

## 12. Cross-language parity exercise

The Security Contracts and Runtime Enforcement parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
