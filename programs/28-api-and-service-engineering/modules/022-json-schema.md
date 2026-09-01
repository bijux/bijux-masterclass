---
module_id: API-022
program: API & Service Engineering
level: 1
module_number: 22
title: JSON Schema
status: complete
last_verified: 2026-09-01
---

# JSON Schema

## One-Page Review

### Governing question

How can a producer state exactly which JSON instances are structurally admissible, under a named dialect and resource-resolution context, without confusing validation with business behavior or authority?

### Essential definitions

- A **JSON instance** is a value from the JSON data model: object, array, string, number, boolean, or null.
- A **schema** is a JSON value, either an object or a boolean, interpreted under a JSON Schema dialect.
- A **dialect** is a collection of vocabularies identified by a meta-schema URI; it determines which keywords and processing rules apply.
- An **assertion** constrains whether an instance is valid, while an **annotation** records information for other processing.
- A **schema resource** is a schema with an identity and base URI; a document can bundle multiple resources.
- An **applicator** applies subschemas to instance locations and combines their results.
- An **evaluation result** includes validity and may include annotations and the instance and schema locations responsible for the result.

### Central model, mechanism, or theorem

Validation is a contextual relation $V(I,S,D,R)$ over instance $I$, schema $S$, dialect $D$, and resource registry or retrieval context $R$. The same schema bytes can be interpreted differently under another dialect or with another referenced resource. A conforming result is not just “true” or “false”: useful output identifies failed keywords and locations, while annotations influence features such as unevaluated-property processing.

### Critical invariants

Every production schema names or inherits one known dialect. Reference resolution uses stable, absolute resource identifiers. Object and array closure is deliberate rather than accidental. Missing, null, and empty remain distinct. Numeric constraints describe mathematical values, not one language's floating-point accidents. Formats are not assumed to assert unless the chosen dialect and validator configuration say so. Defaults and examples do not mutate an instance. Validation happens before authorization and does not prove semantic correctness, safe effects, or contract conformance.

### Common failures

Omitting `$schema`; copying Draft 7 tuple syntax into Draft 2020-12; treating `properties` as requiring fields; treating `required` as checking types; closing every subschema with `additionalProperties: false`; assuming `$ref` is textual inclusion; trusting `format` as universal rejection; confusing absent with `null`; using `oneOf` where branches overlap; expecting `default` to insert data; validating numbers through binary floating point; and calling a valid request authorized.

### Compact example

An order request requires `currency` and `amount`, constrains currency to three uppercase ASCII letters, makes amount a positive multiple of `0.01`, and rejects unevaluated top-level properties. `{"currency":"SEK","amount":12.50}` is structurally valid. The schema does not prove that SEK is supported for the merchant, that the caller may charge, that stock exists, or that the decimal was parsed without loss. **Conclusion:** schema validity is a bounded structural claim inside a larger API contract.

### Connections

[API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) defines the promises that schemas cannot carry alone. [OpenAPI Structure](../ROADMAP.md) embeds Schema Objects in an interface description and introduces an OpenAPI dialect. [Request and Response Modeling](../ROADMAP.md) applies schemas to consumer-owned input and service-owned output.

## Governing Question

How should an API engineer identify, compose, evaluate, and evolve JSON Schemas so that structural validation is interoperable, diagnostic, and correctly bounded?

## Why This Matters

JSON is deliberately small. RFC 8259 defines objects, arrays, strings, numbers, booleans, and null, but it does not say that an order needs an identifier, that a page size is at most 100, or that a tuple has exactly three elements. JSON Schema adds a language for expressing such constraints and metadata. It supports documentation, editors, test generation, client and server validation, compatibility analysis, and reusable contract components.

The phrase “valid JSON” therefore has two different meanings. A text may be syntactically valid JSON yet fail an application schema. Conversely, an instance may pass a schema while being unacceptable in the current domain state. A syntactically and structurally valid refund can still exceed the refundable balance, target another tenant, violate a transition rule, or duplicate an effect. JSON Schema is one contract layer, not the whole contract.

Dialect precision matters. The JSON Schema project identifies Draft 2020-12 as the current version when checked on 2026-09-01. Draft 2020-12 changed tuple keywords, dynamic references, interactions with `contains`, and treatment of `format` compared with earlier drafts. OpenAPI 3.2.0 bases its Schema Object dialect on Draft 2020-12 vocabularies and adds OpenAPI keywords. A validator must know which dialect it is evaluating; merely recognizing familiar keyword spellings is not enough.

Validation can also become a security and reliability boundary. Unbounded regular expressions, deeply nested references, huge arrays, or hostile schemas can consume resources. Remote retrieval can introduce nondeterminism or server-side request risks. Production systems should use reviewed schemas, pinned resources, bounded inputs, controlled registries, and explicit validator capabilities.

## Prerequisites and Retrieval

Retrieve JSON syntax and data types, URI references, JSON Pointer, API contracts, request ownership, mathematical intervals, regular expressions, Unicode, versioning, and testing. Be able to distinguish a JSON text from the in-memory value it represents, an instance from a schema, and a structural constraint from a domain rule.

Before using a schema, retrieve its declared meta-schema, every required vocabulary, the identifiers of referenced resources, the validator's supported dialects, and its format policy. For an embedded OpenAPI Schema Object, also retrieve the enclosing document's `jsonSchemaDialect` and OpenAPI version.

## Learning Objectives

By the end of this module, you should be able to:

1. explain the JSON Schema evaluation model and Draft 2020-12 dialect;
2. constrain objects, arrays, strings, numbers, booleans, and null precisely;
3. compose and reference schemas without confusing inclusion, implication, and alternatives;
4. reason about annotations, evaluated locations, formats, and validator output;
5. separate schema validity from semantic, authorization, and behavioral checks; and
6. design portable schema resources, tests, diagnostics, and evolution rules.

## Core Exposition

### Start with the JSON data model

JSON Schema evaluates JSON values, not source-language objects. JSON has one number category, while a programming language may distinguish integers, binary floating point, arbitrary precision decimals, and special values. JSON objects have string member names. JSON arrays are ordered. JSON has no date, byte-string, set, class, undefined value, comment, or reference type.

RFC 8259 permits insignificant whitespace and escape sequences, and it defines interoperability guidance for numbers and Unicode. Duplicate object names are especially dangerous: implementations have historically differed on whether they retain the last value, report an error, or expose all values. Parse JSON with a policy that rejects duplicates before schema evaluation. A validator operating on an already constructed map cannot recover the discarded duplicate.

The instance and the schema use the same JSON data model. The object schema `{}` admits every instance because it states no failing assertion. The boolean schema `true` also admits every instance, while `false` rejects every instance. Boolean schemas are useful for generated policies and for explicitly closing a position.

### Name the dialect and vocabulary

Put `$schema` at the root of a standalone schema resource:

<!-- bijux-verify: {"id":"dialect-and-resource-identity","mode":"data","language":"json","toolchain":"none","reason":"Declarative JSON Schema resource used to illustrate dialect and identity; it is inspected rather than executed."} -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.example.test/order-request",
  "type": "object"
}
```

`$schema` identifies a meta-schema and therefore a dialect. A dialect selects vocabularies such as Core, Applicator, Validation, Unevaluated, Format Annotation, Content, and Meta-Data. The meta-schema can validate much of a schema's shape, but successful meta-schema validation does not prove that every implementation supports every optional vocabulary or behaves interoperably outside the specification.

Unknown keywords are normally annotations rather than automatic failures. That extensibility is useful, but it makes silent capability mismatch possible. A build should check that the validator recognizes the declared dialect and every vocabulary required by organizational policy. Rejecting an instance after ignoring a security-relevant custom keyword would create a false assurance boundary.

OpenAPI 3.2.0 Schema Objects use an OpenAPI dialect unless a resource-root `$schema` or the enclosing `jsonSchemaDialect` selects another supported dialect. The OpenAPI dialect includes Draft 2020-12 vocabularies and OpenAPI-specific keywords. A standalone JSON Schema validator may treat those extra keywords as unknown annotations. Do not assume that a schema copied between OpenAPI, a database validator, and an independent JSON Schema tool retains identical meaning.

### Establish identity and resolve references

`$id` establishes the canonical URI and base URI of a schema resource. Prefer stable absolute HTTPS identifiers even when no network retrieval is intended. Identity is not the same as a file path. A registry can map the URI to reviewed local bytes, allowing deterministic and offline evaluation.

`$ref` is an applicator that resolves a URI reference and applies the target schema. It is not textual copy-and-paste. Relative references resolve against the current base URI, which can change at nested schema-resource boundaries. A fragment may be a JSON Pointer or a named anchor such as `#money`. `$anchor` provides a plain-name fragment; `$dynamicAnchor` and `$dynamicRef` support dynamic scope for extensible recursive schemas.

Draft 2020-12 permits sibling keywords beside `$ref`; each applies according to its vocabulary. Old advice that every sibling is ignored came from earlier dialect behavior and must not be generalized. Reference cycles are not automatically erroneous—recursive data models need them—but an evaluator must terminate and constrain resource use.

Bundling several schema resources into one JSON document does not erase their identities. Preserve each `$id`, register all resources, and test both bundled and independently retrieved forms. Do not let runtime validation fetch arbitrary network locations. Pin content, restrict schemes and hosts, cap size and depth, and make missing resources a visible configuration failure.

### Constrain object shape and presence

`type: "object"` restricts the instance category. `properties` maps names to schemas, but it does not require those names. `required` lists names that must be present, but it says nothing about their values unless another keyword does. These responsibilities compose:

<!-- bijux-verify: {"id":"object-presence-schema","mode":"data","language":"json","toolchain":"none","reason":"Declarative schema fragment illustrating independent presence and value constraints."} -->
```json
{
  "type": "object",
  "required": ["name", "email"],
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "email": {"type": "string", "format": "email"}
  }
}
```

An absent member, a member whose value is `null`, and an empty string are three different instances. To permit null, include it explicitly, for example `"type": ["string", "null"]`. Do not use nullable fields as an unexamined substitute for omission semantics. State whether omission means unchanged, defaulted, unknown, not applicable, or hidden.

`patternProperties` applies schemas to names matching regular expressions. `propertyNames` constrains member names. `minProperties` and `maxProperties` bound cardinality. `dependentRequired` expresses presence dependencies such as “if `credit_card` appears, `billing_address` must also appear.” `dependentSchemas` applies a whole subschema when a triggering property exists.

`additionalProperties` applies only to properties not covered by `properties` or `patternProperties` in that schema object. It does not see successful evaluation performed by an unrelated branch in the way authors often expect. In composed schemas, `unevaluatedProperties` can close properties that were not successfully evaluated by applicable subschemas. This makes it powerful and subtle: annotation collection and branch success affect the result. Test the exact composition instead of mechanically attaching `additionalProperties: false` everywhere.

Choose openness intentionally. Rejecting unknown request fields catches spelling mistakes and prevents accidental mass assignment. Tolerating unknown response fields supports additive evolution. These are different consumer contracts and should rarely share one schema unchanged.

### Model arrays as lists or tuples

For a homogeneous list in Draft 2020-12, `items` is one schema applied to remaining array elements. `minItems` and `maxItems` constrain length; `uniqueItems` compares complete JSON values for equality and may be expensive on large compound values.

For a tuple, `prefixItems` contains positional schemas. `items` then governs elements after the prefix:

<!-- bijux-verify: {"id":"tuple-schema","mode":"data","language":"json","toolchain":"none","reason":"Declarative Draft 2020-12 tuple schema illustrating prefixItems and closure."} -->
```json
{
  "type": "array",
  "prefixItems": [
    {"const": "point"},
    {"type": "number"},
    {"type": "number"}
  ],
  "items": false
}
```

This admits exactly a three-element tagged point. Earlier drafts used an array-valued `items` plus `additionalItems`; copying that form into Draft 2020-12 changes or invalidates the intended schema.

`contains` requires at least one array element to validate against its subschema by default. `minContains` and `maxContains` refine the number of matching elements and matter only with `contains`. A match is about validation, not merely equality. The matched elements are considered evaluated for interactions with `unevaluatedItems` under Draft 2020-12.

Schema validity cannot establish collection behavior such as stable order, pagination snapshots, or uniqueness in an external database. `uniqueItems` also cannot express uniqueness by one field while ignoring others. Such requirements need application logic or a different representation.

### Treat strings as text, not domain types

`minLength` and `maxLength` count Unicode code points as defined by the validation specification, not UTF-8 bytes and not necessarily what a user perceives as grapheme clusters. A displayed symbol may contain several code points. Enforce transport byte limits separately and use domain-aware libraries for user-visible length policies.

`pattern` uses regular expressions and is not implicitly anchored. Pattern `cat` matches any string containing a matching substring; use `^cat$` when whole-string matching is intended, subject to the dialect's regular-expression rules. Avoid pathological expressions and validator-specific syntax. Test Unicode, empty strings, combining marks, long input, and near misses.

`format` gives semantic labels such as date-time, email, hostname, IPv4, IPv6, URI, and UUID. In the Draft 2020-12 general-purpose meta-schema, format is an annotation vocabulary by default; implementations need not reject an instance merely because its format is invalid. The separate format-assertion vocabulary can require assertion behavior, and tools may expose configuration switches. Contract tests must record which behavior is enabled.

Even asserted format is usually syntactic. An email-shaped string is not proof of a deliverable or controlled mailbox. A URI can be syntactically valid yet unsafe to retrieve. A date-time can be well formed while falling outside a business window. Use format for its defined lexical semantics and apply domain, authority, and network policy separately.

### Preserve exact numeric meaning

`type: "integer"` describes a mathematical integer. In JSON Schema, a numeric instance with zero fractional part can satisfy integer semantics even if its textual form was `1.0`, depending on the instance model supplied by the implementation. Do not infer lexical spelling after parsing.

Use `minimum`, `maximum`, `exclusiveMinimum`, and `exclusiveMaximum` for intervals. Use `multipleOf` for exact divisibility. Decimal monetary steps such as `0.01` require exact decimal or rational arithmetic. A binary floating-point validator can produce surprising results near boundaries. Preserve number tokens into an arbitrary-precision representation or model money as integer minor units when that matches the currency contract.

JSON itself does not admit NaN or infinities. Some language serializers do unless configured strictly. Reject non-JSON numeric values at parsing and serialization boundaries. Also impose digit and magnitude limits before expensive arbitrary-precision processing.

### Compose logic deliberately

`allOf` requires every subschema to succeed. It composes constraints; it does not provide object-oriented inheritance or merge objects. Conflicting branches make the intersection empty. `anyOf` requires at least one branch. `oneOf` requires exactly one branch. `not` inverts a subschema's validity.

Use `oneOf` only when exclusive alternatives are genuinely required. Overlapping branches cause surprising rejection; many validators must evaluate every branch to prove exclusivity, producing noisy diagnostics and extra cost. A tagged union is clearer: require a discriminator-like property with `const` in each branch, then use `oneOf` or `if`/`then` appropriately. The JSON Schema keyword `const` performs the actual constraint; an OpenAPI discriminator is a tooling hint and does not replace validation.

`if` evaluates a condition. `then` applies only when `if` succeeds; `else` applies when it fails. `if` alone does not reject. Make the condition itself precise, often including `required`, because `properties` does not imply presence. Conditional schemas are suitable for structural dependencies, but a large business state machine is usually clearer in application rules and behavioral contract tests.

### Understand annotations and evaluated locations

Keywords such as `title`, `description`, `default`, `examples`, `deprecated`, `readOnly`, and `writeOnly` communicate metadata. They do not generally assert validity. In particular, `default` does not insert a missing value, `readOnly` does not perform authorization, and `writeOnly` does not redact a response. A framework may implement transformations around validation, but that behavior is outside base JSON Schema and must be specified separately.

Annotations from successful subschema evaluation can affect later keywords. `unevaluatedProperties` and `unevaluatedItems` depend on which instance locations were evaluated. This is not equivalent to scanning source text for declared names. Applicator branches, references, and conditionals contribute results according to the specification.

Prefer structured validator output that reports the instance location, keyword location, absolute schema location, error code, and nested causes. A message like “not valid under any schema” is inadequate for a consumer. Do not expose internal schemas or sensitive allowed values indiscriminately, however; translate detailed diagnostics into safe, stable API problems.

### Bound what validation proves

Let $I$ be an instance, $S$ a schema, $D$ a dialect, and $R$ a registry. The statement $V(I,S,D,R)=\mathsf{valid}$ means that the evaluator found no failed assertion under that context. It does not prove that $I$ is true, useful, authorized, current, unique in a database, compatible with every consumer, or safe to execute.

Validation should occur after strict parsing and size limits, and before interpreting untrusted fields as commands. Follow it with normalization only when normalization semantics are explicit, then domain invariants, state preconditions, authorization, rate and abuse policy, and effect control. Be careful with transformations: validating a pre-normalized instance and executing a materially different normalized value can invalidate the evidence. Revalidate the effective value or prove the transformation preserves all required constraints.

The executable fixture below implements only a named subset of object validation. It exists to make presence, type, numeric, and closure rules observable without pretending to be a Draft 2020-12 implementation.

<!-- bijux-verify: {"id":"bounded-schema-subset","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_order=accepted\nmissing_amount=required:amount\nnull_currency=type:currency\nextra_field=unevaluated:note\nzero_amount=exclusiveMinimum:amount\nchecks=5\nevidence=bounded_schema_subset\n","stderr":""}} -->
```python
from decimal import Decimal

schema = {
    "required": ("currency", "amount"),
    "types": {"currency": str, "amount": Decimal},
    "exclusive_minimum": {"amount": Decimal("0")},
    "closed": True,
}

def validate(instance):
    for name in schema["required"]:
        if name not in instance:
            return f"required:{name}"
    for name, expected in schema["types"].items():
        if not isinstance(instance[name], expected):
            return f"type:{name}"
    known = set(schema["types"])
    unknown = set(instance) - known
    if schema["closed"] and unknown:
        return f"unevaluated:{min(unknown)}"
    for name, lower in schema["exclusive_minimum"].items():
        if instance[name] <= lower:
            return f"exclusiveMinimum:{name}"
    return "accepted"

fixtures = {
    "valid_order": {"currency": "SEK", "amount": Decimal("12.50")},
    "missing_amount": {"currency": "SEK"},
    "null_currency": {"currency": None, "amount": Decimal("12.50")},
    "extra_field": {"currency": "SEK", "amount": Decimal("12.50"), "note": "x"},
    "zero_amount": {"currency": "SEK", "amount": Decimal("0")},
}

for label, instance in fixtures.items():
    print(f"{label}={validate(instance)}")
print(f"checks={len(fixtures)}")
print("evidence=bounded_schema_subset")
```

### Test schemas and their consumers

Maintain positive fixtures, negative fixtures, and boundary fixtures. Each negative fixture should fail for a named reason; otherwise an unrelated constraint can mask a missing rule. Include omitted versus null, empty collections, exact bounds, just-outside bounds, Unicode, duplicate names at the parser boundary, extra properties, every alternative branch, ambiguous branches, unresolved references, and large adversarial values.

Run schemas against more than one conforming implementation when portability matters. The official JSON Schema Test Suite is useful implementation evidence, but application schemas need their own fixtures. Record the dialect, validator name and version, enabled formats, resource registry, parsing number model, output format, and limits. A passing schema test is not evidence that request handling actually invokes the same configuration.

Test schema consumers too. Code generators may approximate unions, numeric precision, nullable fields, maps, or recursive structures. Documentation renderers may hide constraints. Mock servers may choose one example and ignore conditionals. Compare generated behavior with the normative schema and retain hand-written behavioral tests for guarantees the schema cannot express.

### Evolve schemas with consumer evidence

Schema implication provides a useful direction: for a request schema, widening the accepted instance set can be producer-compatible while narrowing it can reject existing clients; for a response schema, narrowing produced instances may be consumer-compatible while widening them can surprise strict consumers. Real compatibility also depends on ownership, code generation, defaults, semantics, and observed consumers.

Adding an optional response property is structurally compatible with tolerant readers but breaks clients that reject unknown fields. Adding an enum value widens the schema but can break exhaustive switches. Making a property optional widens request acceptance but may change domain meaning. Changing a pattern, reference target, or format policy can alter the admitted set without changing the top-level file.

Version schema resources and dependencies by immutable identity where reproducibility matters. Produce semantic diffs supplemented by witness instances that changed classification. Test known consumer fixtures, publish deprecation, and avoid overwriting a resource at the same stable `$id` with incompatible meaning. Evolution approval should cover the full API contract, not only the schema diff.

## Definitions and Notation

Let $J$ be the set of JSON instances. A schema resource $S$ is a boolean or object interpreted under dialect $D$. Registry $R$ maps canonical schema URIs to immutable resources. Evaluation can be modeled as:

$$
E_D(I,S,R)=(v,A,O),
$$

where $v\in\{\mathsf{valid},\mathsf{invalid}\}$, $A$ is the collected annotation information, and $O$ is structured output containing instance and schema locations. This model is explanatory; exact output formats and annotation collection follow the applicable specification and implementation capability.

The valid-instance set of a schema is:

$$
L_D(S,R)=\{I\in J\mid E_D(I,S,R).v=\mathsf{valid}\}.
$$

For schemas $S_1$ and $S_2$, $S_1$ is at least as restrictive as $S_2$ when $L_D(S_1,R)\subseteq L_D(S_2,R)$. Deciding implication for arbitrary schemas and implementation extensions may be difficult; bounded counterexample generation and consumer fixtures remain practical evidence.

A **meta-schema** describes a schema dialect. A **vocabulary** is a named set of keywords and semantics. An **assertion** can make evaluation invalid. An **annotation** attaches information to evaluation. An **applicator** applies subschemas. A **schema resource** has an identity and root. A **compound schema document** bundles resources. A **registry** resolves identifiers without implying network access. A **witness instance** demonstrates a classification or compatibility difference.

## Mechanisms, Invariants, or Proof Structure

1. Parse the JSON text strictly, rejecting duplicate object names and non-JSON numbers.
2. Enforce byte, nesting, member, array, string, and numeric-complexity limits.
3. Determine the schema resource, `$schema` dialect, and required vocabularies.
4. Build a controlled registry for every `$id`, anchor, and referenced resource.
5. Evaluate applicators, assertions, and annotations under that exact context.
6. Return structured diagnostics with instance and schema locations.
7. Apply explicit normalization and revalidate the effective instance when required.
8. Enforce domain, state, authority, temporal, and effect rules outside the schema.
9. Test boundaries, alternatives, references, resource limits, and multiple implementations.
10. Evaluate evolution by valid-set direction, consumer behavior, and witness instances.

The central invariants are dialect determinism, resource identity, exact instance semantics, deliberate openness, bounded evaluation, diagnostic traceability, and separation of structural validity from permission and behavior. A review should be able to reproduce the result from the instance, schema, dialect, registry, parser policy, validator configuration, and limits.

## Alternatives and Trade-Offs

Inline schemas are easy to read locally but duplicate definitions and drift. Referenced resources improve reuse and identity but require disciplined URI resolution and deployment. Bundling enables offline evaluation while preserving resource identities; careless bundling changes base URIs and breaks references.

Open object schemas ease response evolution and tolerate producer additions. Closed request schemas catch mistakes and narrow the writable surface. Uniformly open schemas hide typos; uniformly closed schemas make composition and response evolution brittle. Choose by ownership and direction rather than one organization-wide boolean.

`anyOf` permits overlap and often gives simpler evolution. `oneOf` enforces exclusivity but demands disjoint branches and more evaluation. Tagged unions make branch selection clearer but place a stable tag in the representation. Conditionals express local dependencies well; application state machines better express history, authority, and external facts.

String encodings for money and timestamps preserve lexical control but shift parsing into application code. JSON numbers are natural for measurements yet require an exact numeric model for decimal constraints. Integer minor units are precise but currency-dependent. Select a representation from domain range, precision, interoperability, and evolution needs.

Validation at the edge rejects bad input early and gives consistent diagnostics. Validation only inside services risks divergent behavior; validation only in a gateway can be bypassed and cannot cover state. Use defense in depth without letting two schemas drift. Generated validators can be fast and typed but may implement only a subset; general evaluators are flexible but need capability and resource controls.

## Failure Modes and Misconceptions

- **“The JSON parsed, so it is valid.”** Parsing establishes JSON syntax; schema evaluation establishes only declared structural assertions.
- **“`properties` makes fields mandatory.”** It applies subschemas when names exist; `required` establishes presence.
- **“`required` rejects null.”** Presence and value constraints are separate; apply `type` or another schema to the value.
- **“`$ref` pastes an object here.”** It resolves and evaluates a schema resource or subschema under URI rules.
- **“Every `$ref` sibling is ignored.”** That is obsolete as a general claim for Draft 2020-12.
- **“`additionalProperties: false` closes an inherited object.”** Its coverage is local; composition often needs deliberate `unevaluatedProperties` design.
- **“`format: email` always rejects malformed values.”** Draft 2020-12 distinguishes annotation and assertion vocabularies, and tool configuration matters.
- **“`default` fills missing input.”** It is an annotation unless a surrounding tool defines transformation behavior.
- **“`readOnly` enforces access control.”** It documents directionality for tooling; authorization remains an application obligation.
- **“`oneOf` chooses the first branch.”** It requires exactly one successful branch; overlap invalidates the instance.
- **“A JSON number is a safe floating-point value.”** JSON is not limited to one machine representation; preserve required precision.
- **“A valid request is safe to execute.”** Schema cannot establish current state, authority, uniqueness, external reachability, or effect semantics.
- **“Remote `$ref` means the validator should fetch the web.”** Production resolution should be controlled, pinned, bounded, and usually offline.
- **“Passing one validator proves portability.”** Dialect support, formats, number models, extensions, and output behavior differ.
- **“An additive schema edit cannot break clients.”** Generated and strict consumers, exhaustive enums, semantics, and defaults can still break.

## Worked Examples

### Example 1

**Situation:** A request schema lists `name` under `properties`, but `{}` passes. **Reasoning:** `properties` constrains a value only when that member exists. Add `"required": ["name"]` and keep the string constraint. **Conclusion:** presence and value validity are orthogonal.

### Example 2

**Situation:** `nickname` can be absent but cannot be null. **Reasoning:** Use no `required` entry for it and retain `"type": "string"`. Adding `null` to the type would create a third admitted state. **Conclusion:** omission is not nullability.

### Example 3

**Situation:** A three-position coordinate schema copied from Draft 7 uses array-valued `items`. **Reasoning:** Under Draft 2020-12 use three `prefixItems` schemas and `items: false`. Declare `$schema` so tooling cannot guess. **Conclusion:** dialect migrations can change keyword shape and meaning.

### Example 4

**Situation:** An address base schema is combined with a country branch, and `additionalProperties: false` in the base rejects the branch's `region`. **Reasoning:** The closure keyword in the base does not automatically recognize properties declared elsewhere. Restructure the object or apply `unevaluatedProperties: false` at the intended composition boundary and test annotations. **Conclusion:** object closure is a composition decision.

### Example 5

**Situation:** A `oneOf` permits `{ "kind": "card" }` under two branches. **Reasoning:** Both succeed, so `oneOf` fails. Give each branch a distinct required `kind` value with `const`, or use `anyOf` if overlap is acceptable. **Conclusion:** exclusivity must be designed, not assumed.

### Example 6

**Situation:** A validator accepts `format: "date-time"` nonsense in one environment but rejects it in another. **Reasoning:** One treats format as annotation and the other enables assertion. Pin the dialect, vocabulary capability, and validator configuration in tests. **Conclusion:** format policy is part of the validation context.

### Example 7

**Situation:** An amount must be a multiple of `0.01`, but binary floating-point evaluation rejects an expected value. **Reasoning:** Parse and compare using decimal or rational arithmetic, or model agreed integer minor units. **Conclusion:** mathematical schema constraints require an adequate instance number model.

### Example 8

**Situation:** A schema references `customer.json`, and staging resolves a different file than production. **Reasoning:** Give the resource an absolute `$id`, pin its bytes in a registry, and resolve the relative reference from a known base. **Conclusion:** reference reproducibility depends on identity and controlled resolution.

### Example 9

**Situation:** `default: "standard"` appears on `tier`, but the validated instance still lacks `tier`. **Reasoning:** `default` is annotation. Define an explicit defaulting transformation, apply it before the domain decision, and validate the effective value. **Conclusion:** annotation is not mutation.

### Example 10

**Situation:** A transfer request passes every schema check but targets an account the caller does not control. **Reasoning:** Structural validity admits the message shape; object-level authorization must reject the action without disclosing protected facts. **Conclusion:** schema validation precedes but never replaces authority checks.

## Cross-Program Connections

[Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains interpretation under an explicit language and environment. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies tree, map, and recursion costs. [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies language inclusion and counterexample reasoning. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies hostile-input, authorization, and retrieval-threat models. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains why structural acceptance cannot establish current cross-service facts. The API program composes these into a public validation boundary.

## References

1. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), 16 June 2022. Checked 2026-09-01.
2. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
3. JSON Schema, [*Draft 2020-12 Release Notes*](https://json-schema.org/draft/2020-12/release-notes), including array, dynamic-reference, contains, and format changes. Checked 2026-09-01.
4. T. Bray, [*RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format*](https://www.rfc-editor.org/rfc/rfc8259.html), Internet Standard, December 2017. Checked 2026-09-01.
5. P. Bryan, K. Zyp, and M. Nottingham, [*RFC 6901: JavaScript Object Notation (JSON) Pointer*](https://www.rfc-editor.org/rfc/rfc6901.html), Standards Track, April 2013. Checked 2026-09-01.
6. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), 19 September 2025. Latest published version and Schema Object dialect checked 2026-09-01.

## Exercises

### Exercise 1

Write a Draft 2020-12 schema for a create-user request requiring `displayName` and `email`, rejecting unknown top-level fields, permitting an optional non-null array of one to five distinct role strings, and naming a stable resource identity. Explain what the schema does not prove.

### Exercise 2

Diagnose this intended tagged union: `oneOf` contains two object branches, both with optional `kind` and unrelated optional fields. Construct an overlapping witness, then repair the union for `card` and `bank` alternatives.

### Exercise 3

A base resource schema closes with `additionalProperties: false`; an `allOf` extension adds `createdAt`, which is rejected. Explain why and present two coherent restructuring choices, including the trade-off of `unevaluatedProperties`.

### Exercise 4

Design a validation evidence matrix for a payment amount with exclusive lower bound zero, upper bound 10,000, and cent precision. Include number parsing, boundary, hostile-size, and business-rule cases.

### Exercise 5

A team changes a response schema by adding an enum value, allowing an extra object property, changing an email format from annotation to assertion, and republishing a referenced schema at the same `$id`. Analyze structural and operational compatibility and propose a controlled rollout.

## Answers to the Exercises

### Answer 1

Use `$schema: "https://json-schema.org/draft/2020-12/schema"`, a stable absolute `$id`, `type: "object"`, `required: ["displayName", "email"]`, and property schemas for two non-empty strings. Define `roles` as an array with `items: {"type":"string"}`, `minItems: 1`, `maxItems: 5`, and `uniqueItems: true`; omit null from its type. Apply `unevaluatedProperties: false` or, without composition, `additionalProperties: false` at the object boundary. It does not prove mailbox control, role existence, role-grant authority, name policy, uniqueness, current quota, or safe creation effects.

### Answer 2

`{}` is an overlapping witness because both branches can succeed when every property is optional. Require `kind` in both branches and constrain it with `const: "card"` or `const: "bank"`. Add each branch's required fields, place common properties deliberately, and close the intended outer boundary. Now the tags make branches disjoint. If multiple classifications were legitimate, `anyOf` would better express the contract than artificial exclusivity.

### Answer 3

`additionalProperties` accounts for properties declared in its own schema object; it does not treat the extension's `createdAt` declaration as local. One choice is to move all property declarations and closure to one object schema, sacrificing independently closed inheritance. Another is to compose open component schemas and place `unevaluatedProperties: false` at the outer boundary, which can recognize successfully evaluated locations across applicable branches but requires correct Draft 2020-12 annotation behavior and stronger tool support. Test positive, unknown, failed-branch, and reference cases.

### Answer 4

Use exact decimal parsing and test `0`, the smallest admitted cent, an ordinary value, `10000`, and a value just above; state whether the upper bound is inclusive. Test excessive fractional precision against `multipleOf: 0.01`, negative zero policy, exponent notation, huge digit counts, non-JSON NaN/infinity tokens, and parser duplicate-name handling around the containing object. Then separate structural cases from unsupported currency, merchant limits, available balance, authorization, and duplicate-effect rules. Record the dialect, validator version, number model, and limits.

### Answer 5

The enum addition and extra property widen the response instance set but can break exhaustive or strict consumers. Enabling format assertion can newly reject producer output or fixtures and must be treated as a validation-policy change. Replacing bytes behind one `$id` destroys reproducibility and may silently change every referrer. Inventory consumers and validators, publish immutable resource identities, add tolerant-reader and unknown-enum handling, validate existing production examples under both versions, generate witness instances, stage provider and consumer changes, and retain the previous resource through the declared compatibility window. Review behavioral meaning separately from schema inclusion.
