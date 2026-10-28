# Reference Answers — Module 09: Evolution, Compatibility, and Audience Views

Read after attempting all twelve Evolution, Compatibility, and Audience Views exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why can adding a response enum value be breaking?

Old consumers may use exhaustive decoders or switches that reject or mishandle an unknown value, even though the schema change is additive.

## 2. Is removing a maximum from a request string compatible?

It widens what the new provider accepts, so old consumers still work with the new provider. A new consumer may send longer values that an old provider rejects; direction matters.

## 3. Is adding a required response property breaking?

Often old consumers tolerate it, but exact decoders, signatures, generated constructors, and snapshots may fail. Classify it with consumer policy rather than a universal answer.

## 4. Why is changing operationId risky without wire change?

Generated source names, links, Arazzo references, documentation anchors, and tests can depend on the identifier.

## 5. What belongs in a deprecation record?

Affected element, replacement, first deprecated release, support/removal date or condition, migration example, telemetry/owner, and planned major version.

## 6. Why archive a bundle rather than only modular source?

Consumers and diff gates need the exact resolved publication artifact; reference resolution and remote content can otherwise change.

## 7. What must an Overlay output test assert?

Successful application, expected server/metadata updates, required operation set, forbidden internal paths/tags/schemas, reference validity, and deterministic digest.

## 8. Design a breaking-gate self-test.

Compare a known good release to a fixture that removes a response, renames an operationId, and narrows a constraint; require non-zero exit and all categories in the report.

## 9. When may a suppression be defensible?

For a precisely identified false positive or accepted context-specific risk, with rationale, affected consumers, owner, limited scope, and expiration/release boundary.

## 10. Why is semantic versioning alone insufficient?

A version label communicates intent but does not select runtime behavior, detect changes, preserve artifacts, or supply migration evidence.

## 11. Practical defect exercise

For **All additions called safe**, a valid solution must first reproduce: new enum/status/field breaks a strict consumer. The smallest useful starting case is: regenerate or run an exhaustive consumer fixture. The repair is: Review direction and representative client assumptions.

## 12. Cross-language parity exercise

The Compatibility, Releases, Overlay, and CI parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
