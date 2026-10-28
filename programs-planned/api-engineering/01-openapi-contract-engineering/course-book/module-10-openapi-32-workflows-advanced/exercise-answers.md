# Worked Answers — Module 10: OpenAPI 3.2, Streaming, Webhooks, and Workflows

Use these solutions to audit your reasoning for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why keep 3.1.2 and 3.2.0 artifacts?

The baseline maximizes executable tool compatibility; the frontier teaches and measures current features. Shared identity plus an explicit promotion policy avoids both stagnation and overclaiming.

The chapter’s decisive distinction is this: The executable baseline uses OpenAPI 3.1.2 because the selected generators and framework integrations have broad 3.1 support. The frontier description upgrades the same API to 3.2.0 and exercises current constructs. The two artifacts share operation identity and domain semantics; the frontier is not a speculative rewrite.

## 2. What must “supports 3.2” specify?

Which tool/version, feature, and stage: parsing, validation, rendering, generation, mocking, testing, or runtime routing.

In the cumulative capstone, the rule becomes concrete: “Supports OpenAPI 3.2” can mean parses the version string, validates new fields, renders them, generates clients, mocks behavior, or tests a live provider. The report probes each material feature and stage separately with exact tool versions and commands.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 3. When is `in: querystring` appropriate?

When the complete query component has meaningful grammar/order or must be treated as one value; ordinary named filters should remain normal query parameters.

A useful way to reason about the boundary is: A 3.2 Parameter Object with in: querystring models the entire query string as one value rather than independent named parameters. This can describe structured query languages or signatures where order and whole-string grammar matter. It is not a replacement for ordinary named query parameters.

## 4. What does `itemSchema` not describe?

Transport framing, event delimiters, reconnect behavior, heartbeats, backpressure, or the entire stream as one instance.

The implementation consequence is: The capstone documents SSE and NDJSON progress. itemSchema describes each progress event, while prose and examples define data: framing or newline separation. A validator that only checks the whole byte stream as JSON is the wrong proof tool.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 5. Distinguish callback, webhook, and link.

Callback: provider invokes a request-derived URL after/around an operation. Webhook: an inbound event operation described at the root. Link: a relationship supplying parameters for another operation, not an invocation.

The important nuance is: A callback is an operation the provider may invoke at a URL derived from the initiating request. A root-level webhook describes an inbound event operation that may occur independently of one specific operation declaration. A Link Object describes how response data supplies parameters for another API operation; it does not send a request.

## 6. What could make a runtime expression fragile?

Selecting an optional field, assuming one response branch, wrong JSON Pointer escaping, changed operation response shape, or dependence on normalized headers/URLs.

Under concurrency or failure, the distinction becomes: Runtime expressions can extract values from request URLs, parameters, bodies, response headers, and response bodies. They are used in callback keys and Link parameters. The expression is evaluated against a concrete exchange, so the selected value must exist in every response branch where the link appears.

## 7. What must an Arazzo source description reference provide?

A resolvable OpenAPI source whose operationIds and schemas support the workflow’s step operation references, parameters, request bodies, outputs, and criteria.

The design remains honest only if: An Arazzo document references source descriptions, declares workflows, accepts inputs, executes operation steps, captures outputs, and expresses dependencies or success criteria. It is not an orchestration engine, test framework, or replacement for the OpenAPI contract.

**Evidence.** Move the source tree, resolve every reference offline, build twice, and compare the deterministic bundle and operation inventory.

## 8. How do you test enhanced tag hierarchy?

Validate every parent resolves to a distinct tag, detect cycles, confirm operations reference existing tags, and inspect renderer output separately.

The consumer-facing consequence is: OpenAPI 3.2 Tag Objects can carry a short summary, a parent relationship, and a kind classification. This supports navigable domain groupings without proprietary display extensions. Parent references must point to existing tag names and must not form cycles.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 9. What capability state applies when npm cannot be installed?

Not executed. Installation/network failure is not evidence that the tool semantically lacks support.

The operational consequence is: Results use supported, partial, transformed, unsupported, or not executed. A failed installation is not evidence of unsupported semantics; it is reported as not executed. This distinction is essential when course artifacts are reviewed outside the author’s environment.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 10. Give a safe and unsafe degradation example.

Ignoring `summary` in a tag may be safe presentational loss. Dropping a QUERY operation or sequential item schema is functional/validation loss and needs a fallback or block.

The strongest engineering interpretation is: Streaming formats such as server-sent events, JSON Lines, and JSON text sequences carry a sequence of logical items rather than one JSON document. OpenAPI 3.2’s Media Type Object can describe individual items with itemSchema. The enclosing media type and framing rules still matter.

## 11. Practical defect exercise

For **Version bump only**, a valid solution must first reproduce: document says 3.2 but no new feature is understood or tested. The smallest useful starting case is: insert malformed enhanced tag or query structure. The repair is: Use a 3.2-aware validator and feature probes.

The defect-oriented view is: A valid 3.1 description is intended to remain valid under 3.2, while new 3.2 fields require 3.2-aware tooling. Upgrade begins by changing the version and running a 3.2-aware validator before adopting new syntax. Existing semantics are preserved unless the author deliberately changes them.

## 12. Cross-language parity exercise

The OpenAPI 3.2, Streaming, and Arazzo Workflows parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: For OpenAPI 3.2, Streaming, and Arazzo Workflows, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.
