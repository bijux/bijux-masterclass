# Worked Answers — Module 03: JSON Schema Contract Modeling

Use these solutions to audit your reasoning for **JSON Schema Contract Modeling**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. List the four distinct instances for a `description` property: missing, null, empty, non-empty.

They are `{}`, `{"description": null}`, `{"description": ""}`, and a non-empty string. Requiredness, type, and length constraints classify them independently.

The chapter’s decisive distinction is this: A TypeScript type is erased at runtime, and a Python annotation does not validate arbitrary network bytes by itself. Runtime libraries must parse and validate. Generated types can still misrepresent unions, formats, or additional properties, so fixtures are run through an independent JSON Schema validator and both provider boundaries.

## 2. Design required-but-nullable `completedAt`.

Include `completedAt` in the object `required` list and give its schema a union such as `type: [string, "null"]` with date-time format on the string branch.

In the cumulative capstone, the rule becomes concrete: JSON Schema defines format vocabularies, but an implementation can collect format as annotation without rejecting invalid strings. OpenAPI tooling also varies. A contract that requires a valid date-time or URI must state its enforcement policy and test the selected validators.

## 3. Why does `default: normal` not guarantee the provider receives `priority`?

Default is an annotation and validators need not insert it. The provider must explicitly default or require the property.

A useful way to reason about the boundary is: This JSON Schema 2020-12 Contract Modeling increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.

**Evidence.** Run the same consumer workflow and provider-neutral scenario against the mock, Python provider, and TypeScript provider.

## 4. Create an instance that would expose overlapping local/remote source branches.

Without distinct const tags, an object containing both file and URI properties might satisfy both open branches. The tagged closed design prevents that.

The implementation consequence is: Without an applicator restricting extra properties, object schemas generally allow unknown members. Closing request objects detects typos and over-posting. Closing response objects prevents unreviewed fields from leaking but can make additive evolution harder for strict consumers.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 5. When is `additionalProperties` a schema rather than `false`?

For intentional maps, such as labels whose keys are user-defined but whose values must be bounded strings.

The important nuance is: For JSON Schema 2020-12 Contract Modeling, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

**Counterexample.** A valid-looking example or generated type accepts an instance that the normative schema rejects, or the runtime serializes undeclared state.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 6. Explain `anyOf` versus `oneOf` with set language.

`anyOf` accepts the union of branch sets, including overlap. `oneOf` accepts instances in exactly one branch and excludes the overlap.

Under concurrency or failure, the distinction becomes: Creation input should not accept id, ownerId, timestamps, version counters, artifact IDs, or status chosen by the server. Response models should include the server-owned fields consumers need. Reusing one broad schema in both directions creates over-posting or optionalizes essential response data.

**Evidence.** Add valid and invalid instances to the shared schema fixture corpus and verify independent schema validation plus request and response behavior in both providers.

## 7. Why separate `ProjectCreate` and `Project`?

The request must not accept server-owned ID, owner, version, or timestamps, while the response should require them.

The design remains honest only if: Creation input should not accept id, ownerId, timestamps, version counters, artifact IDs, or status chosen by the server. Response models should include the server-owned fields consumers need. Reusing one broad schema in both directions creates over-posting or optionalizes essential response data.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 8. Write a boundary fixture for `maxLength: 80`.

Use exactly 80 characters as valid and 81 as invalid; also test the minimum independently.

The consumer-facing consequence is: For JSON Schema 2020-12 Contract Modeling, requirements may come from OpenAPI, JSON Schema, HTTP semantics, an observed tool boundary, or the capstone architecture. Keep those sources separate: do not present a local preference as an OpenAPI MUST or soften a normative rule into style.

**Evidence.** Capture the raw HTTP exchange and compare its method, parameters, media type, status, headers, and schema with the resolved operation contract and both providers.

## 9. What can a generated TypeScript type fail to enforce?

Runtime bytes, formats, numeric bounds, patterns, additional-property closure, and exact oneOf logic unless a runtime validator is invoked.

The operational consequence is: A TypeScript type is erased at runtime, and a Python annotation does not validate arbitrary network bytes by itself. Runtime libraries must parse and validate. Generated types can still misrepresent unions, formats, or additional properties, so fixtures are run through an independent JSON Schema validator and both provider boundaries.

## 10. How do you prove validator agreement?

Use one manifest of expected-valid/invalid fixtures and execute it through the independent Draft 2020-12 validator plus both provider request boundaries.

The strongest engineering interpretation is: For every JSON Schema 2020-12 Contract Modeling claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

## 11. Practical defect exercise

For **Optional confused with nullable**, a valid solution must first reproduce: a property is omitted from `required` when the intent was required-but-nullable. The smallest useful starting case is: compare `{}` with `{"completedAt": null}`. The repair is: Model presence and type independently.

The defect-oriented view is: For JSON Schema 2020-12 Contract Modeling, correct-looking YAML and green happy paths remain weak evidence. Start from falsification: every listed defect has an observable symptom, a minimal reproducer, and a bounded repair.

## 12. Cross-language parity exercise

The JSON Schema 2020-12 Contract Modeling parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.

Across the Python and TypeScript tracks, the invariant is: This JSON Schema 2020-12 Contract Modeling increment is a vertical slice: contract source, provider behavior, consumer impact, tests, and evidence move together. A large YAML diff with no executable observation is not progress.
