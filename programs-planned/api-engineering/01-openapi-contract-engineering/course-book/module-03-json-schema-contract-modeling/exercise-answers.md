# Reference Answers — Module 03: JSON Schema Contract Modeling

Read after attempting all twelve JSON Schema Contract Modeling exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. List the four distinct instances for a `description` property: missing, null, empty, non-empty.

They are `{}`, `{"description": null}`, `{"description": ""}`, and a non-empty string. Requiredness, type, and length constraints classify them independently.

## 2. Design required-but-nullable `completedAt`.

Include `completedAt` in the object `required` list and give its schema a union such as `type: [string, "null"]` with date-time format on the string branch.

## 3. Why does `default: normal` not guarantee the provider receives `priority`?

Default is an annotation and validators need not insert it. The provider must explicitly default or require the property.

## 4. Create an instance that would expose overlapping local/remote source branches.

Without distinct const tags, an object containing both file and URI properties might satisfy both open branches. The tagged closed design prevents that.

## 5. When is `additionalProperties` a schema rather than `false`?

For intentional maps, such as labels whose keys are user-defined but whose values must be bounded strings.

## 6. Explain `anyOf` versus `oneOf` with set language.

`anyOf` accepts the union of branch sets, including overlap. `oneOf` accepts instances in exactly one branch and excludes the overlap.

## 7. Why separate `ProjectCreate` and `Project`?

The request must not accept server-owned ID, owner, version, or timestamps, while the response should require them.

## 8. Write a boundary fixture for `maxLength: 80`.

Use exactly 80 characters as valid and 81 as invalid; also test the minimum independently.

## 9. What can a generated TypeScript type fail to enforce?

Runtime bytes, formats, numeric bounds, patterns, additional-property closure, and exact oneOf logic unless a runtime validator is invoked.

## 10. How do you prove validator agreement?

Use one manifest of expected-valid/invalid fixtures and execute it through the independent Draft 2020-12 validator plus both provider request boundaries.

## 11. Practical defect exercise

For **Optional confused with nullable**, a valid solution must first reproduce: a property is omitted from `required` when the intent was required-but-nullable. The smallest useful starting case is: compare `{}` with `{"completedAt": null}`. The repair is: Model presence and type independently.

## 12. Cross-language parity exercise

The JSON Schema 2020-12 Contract Modeling parity scenario must be data-driven by base URL and credentials. Assert observable status, media type, stable headers, schema properties, lifecycle, or authorization—not internal classes. Validate and capture generated identifiers or timestamps instead of comparing fresh literal values.
