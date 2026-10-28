# Worked Answers — Module 09: Evolution, Compatibility, and Audience Views

Use these solutions to audit your reasoning for **Evolution, Compatibility, and Audience Views**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why can adding a response enum value be breaking?

Old consumers may use exhaustive decoders or switches that reject or mishandle an unknown value, even though the schema change is additive.

The chapter’s decisive distinction is this: For request schemas, loosening a maximum or adding an accepted enum value generally widens provider acceptance. For response schemas, emitting values outside the old contract widens provider output and may break old consumers. Adding a required response property is often wire-compatible for tolerant consumers but can break exact decoders, generated constructors, signatures, or snapshots.

## 2. Is removing a maximum from a request string compatible?

It widens what the new provider accepts, so old consumers still work with the new provider. A new consumer may send longer values that an old provider rejects; direction matters.

In the cumulative capstone, the rule becomes concrete: A provider receives requests and emits responses; a consumer emits requests and receives responses. Widening what the provider accepts is usually request-compatible, while widening what it emits can break strict consumers. Making a request field optional may help new callers but can conflict with old providers if a consumer starts omitting it.

## 3. Is adding a required response property breaking?

Often old consumers tolerate it, but exact decoders, signatures, generated constructors, and snapshots may fail. Classify it with consumer policy rather than a universal answer.

A useful way to reason about the boundary is: For request schemas, loosening a maximum or adding an accepted enum value generally widens provider acceptance. For response schemas, emitting values outside the old contract widens provider output and may break old consumers. Adding a required response property is often wire-compatible for tolerant consumers but can break exact decoders, generated constructors, signatures, or snapshots.

## 4. Why is changing operationId risky without wire change?

Generated source names, links, Arazzo references, documentation anchors, and tests can depend on the identifier.

The implementation consequence is: Changing an operationId does not alter HTTP routing, yet generated client methods, Arazzo references, links, tests, and documentation anchors may break. Treat it as a consumer-facing rename. A compatibility gate should report it even if a pure wire diff might not.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 5. What belongs in a deprecation record?

Affected element, replacement, first deprecated release, support/removal date or condition, migration example, telemetry/owner, and planned major version.

The important nuance is: deprecated: true communicates intent but does not identify replacement, timeline, telemetry, or removal conditions. A useful deprecation plan names affected operations or fields, replacement path, first deprecated release, support window, migration examples, and planned major version.

**Evidence.** Diff the old and candidate contract in the correct request/response direction, then run active consumer or generated-client checks before promotion.

## 6. Why archive a bundle rather than only modular source?

Consumers and diff gates need the exact resolved publication artifact; reference resolution and remote content can otherwise change.

Under concurrency or failure, the distinction becomes: The course stores both machine report and reviewer decision. Suppression requires an exact rule, rationale, affected consumers, and expiration or release scope. A clean diff is evidence, not proof that no consumer can break.

**Evidence.** Move the source tree, resolve every reference offline, build twice, and compare the deterministic bundle and operation inventory.

## 7. What must an Overlay output test assert?

Successful application, expected server/metadata updates, required operation set, forbidden internal paths/tags/schemas, reference validity, and deterministic digest.

The design remains honest only if: An Overlay document applies ordered actions to a target OpenAPI description using JSONPath selection. It can update servers or descriptions and remove internal paths for a public or partner view. The target remains canonical; the overlay records the transformation intent.

**Evidence.** Diff the old and candidate contract in the correct request/response direction, then run active consumer or generated-client checks before promotion.

## 8. Design a breaking-gate self-test.

Compare a known good release to a fixture that removes a response, renames an operationId, and narrows a constraint; require non-zero exit and all categories in the report.

The consumer-facing consequence is: A useful gate names the baseline and candidate digests, exact paths/pointers, change classification, policy outcome, and remediation. “Breaking changes found” without locations wastes review time. The attempted minor fixture includes three independent defects so the report must find all three rather than stop at the first.

## 9. When may a suppression be defensible?

For a precisely identified false positive or accepted context-specific risk, with rationale, affected consumers, owner, limited scope, and expiration/release boundary.

The operational consequence is: The course stores both machine report and reviewer decision. Suppression requires an exact rule, rationale, affected consumers, and expiration or release scope. A clean diff is evidence, not proof that no consumer can break.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 10. Why is semantic versioning alone insufficient?

A version label communicates intent but does not select runtime behavior, detect changes, preserve artifacts, or supply migration evidence.

The strongest engineering interpretation is: URI versions create explicit parallel resources but can duplicate surface area. Header or media-type versions keep URIs stable but complicate discovery, caching, and tooling. Semantic artifact versions communicate release intent but do not select runtime behavior alone.

**Evidence.** Diff the old and candidate contract in the correct request/response direction, then run active consumer or generated-client checks before promotion.

## 11. Practical defect exercise

For **All additions called safe**, a valid solution must first reproduce: new enum/status/field breaks a strict consumer. The smallest useful starting case is: regenerate or run an exhaustive consumer fixture. The repair is: Review direction and representative client assumptions.

The defect-oriented view is: A new optional request field is often safe. A new response field can break clients that reject unknown properties. A new enum response member can break exhaustive switches. A new success status may bypass code expecting one exact branch. A new optional security alternative may weaken policy if misunderstood.

## 12. Cross-language parity exercise

The Compatibility, Releases, Overlay, and CI parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: For Compatibility, Releases, Overlay, and CI, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.
