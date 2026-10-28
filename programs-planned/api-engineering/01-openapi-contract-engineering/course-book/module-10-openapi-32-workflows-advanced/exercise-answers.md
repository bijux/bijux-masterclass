# Reference Answers — Module 10: OpenAPI 3.2, Streaming, Webhooks, and Workflows

Read after attempting all twelve OpenAPI 3.2, Streaming, Webhooks, and Workflows exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why keep 3.1.2 and 3.2.0 artifacts?

The baseline maximizes executable tool compatibility; the frontier teaches and measures current features. Shared identity plus an explicit promotion policy avoids both stagnation and overclaiming.

## 2. What must “supports 3.2” specify?

Which tool/version, feature, and stage: parsing, validation, rendering, generation, mocking, testing, or runtime routing.

## 3. When is `in: querystring` appropriate?

When the complete query component has meaningful grammar/order or must be treated as one value; ordinary named filters should remain normal query parameters.

## 4. What does `itemSchema` not describe?

Transport framing, event delimiters, reconnect behavior, heartbeats, backpressure, or the entire stream as one instance.

## 5. Distinguish callback, webhook, and link.

Callback: provider invokes a request-derived URL after/around an operation. Webhook: an inbound event operation described at the root. Link: a relationship supplying parameters for another operation, not an invocation.

## 6. What could make a runtime expression fragile?

Selecting an optional field, assuming one response branch, wrong JSON Pointer escaping, changed operation response shape, or dependence on normalized headers/URLs.

## 7. What must an Arazzo source description reference provide?

A resolvable OpenAPI source whose operationIds and schemas support the workflow’s step operation references, parameters, request bodies, outputs, and criteria.

## 8. How do you test enhanced tag hierarchy?

Validate every parent resolves to a distinct tag, detect cycles, confirm operations reference existing tags, and inspect renderer output separately.

## 9. What capability state applies when npm cannot be installed?

Not executed. Installation/network failure is not evidence that the tool semantically lacks support.

## 10. Give a safe and unsafe degradation example.

Ignoring `summary` in a tag may be safe presentational loss. Dropping a QUERY operation or sequential item schema is functional/validation loss and needs a fallback or block.

## 11. Practical defect exercise

For **Version bump only**, a valid solution must first reproduce: document says 3.2 but no new feature is understood or tested. The smallest useful starting case is: insert malformed enhanced tag or query structure. The repair is: Use a 3.2-aware validator and feature probes.

## 12. Cross-language parity exercise

The OpenAPI 3.2, Streaming, and Arazzo Workflows parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
