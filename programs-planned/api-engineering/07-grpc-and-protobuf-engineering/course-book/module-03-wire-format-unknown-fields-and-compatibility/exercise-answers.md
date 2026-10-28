# Worked Answers — Module 03: Wire Format, Unknown Fields, and Compatibility Discipline

Use these solutions to audit your reasoning for **Wire Format, Unknown Fields, and Compatibility Discipline**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is reusing a removed field number more dangerous than reusing a local variable name?

Retained bytes encode the number, not the old name. Reuse can make historical data parse as a new semantic value without any syntax error.

**Decisive evidence:** tag-reuse golden fixture

The chapter’s decisive distinction is this: Protobuf does not put field names on the binary wire. It encodes field numbers and wire types. Once a field is published, its number is the durable identity. Renaming a field can leave binary compatibility intact while breaking source and ProtoJSON consumers. Reusing a removed number for a new meaning can make retained bytes parse as the wrong value—one of the most dangerous changes in a schema-driven system.

## 2. Classify renaming a field while keeping its tag across four compatibility dimensions.

Binary wire can remain compatible; regenerated source breaks at the accessor name; ProtoJSON keys change; behavior may remain neutral if meaning is identical. The release is not simply compatible.

**Decisive evidence:** four-axis compatibility report

In the cumulative capstone, the rule becomes concrete: Renaming dataset name while retaining tag 3 may be binary compatible, source breaking after regeneration, JSON breaking for clients that send the old key, and behaviorally neutral. Adding an enum value is wire additive but can break exhaustive source code and business assumptions. Increasing a maximum page or chunk size may be schema-neutral yet behaviorally affect memory and scheduling. Changing default deadline policy may not touch the .

## 3. Why is `int32` to `sint32` unsafe despite both representing integers?

`sint32` uses zig-zag encoding while `int32` uses ordinary varint interpretation. Existing bytes produce different values, especially for negatives.

**Decisive evidence:** wire-type vector

A useful way to reason about the boundary is: A field key combines the number with a wire type. Varints, fixed-width values, length-delimited data, and groups have different encodings. Some source-type changes share a wire type and appear binary-readable but reinterpret values. int32, uint32, bool, and enums all use varints, yet changing among them can alter negative values, validation, and meaning. int32 to sint32 is especially unsafe because zig-zag encoding changes the bytes' interpretation even though both are integer concepts.

## 4. When may an old intermediary safely drop unknown fields?

Only when the component semantically consumes and reconstructs the message and the contract does not promise transparent forwarding or exact-byte retention. A relay/archive may not drop them.

**Decisive evidence:** unknown-field forwarding test

The implementation consequence is: An older consumer may receive a newer field it does not know. A well-behaved binary runtime can preserve that field when parsing and reserializing the message, allowing an old intermediary to forward new data without destroying it. But preservation is not universal across transformations. Converting to a domain object, rebuilding a message, passing through JSON, or using certain dynamic libraries may drop unknown fields.

## 5. Classify adding a new enum value for a TypeScript consumer with an exhaustive switch.

Wire-additive but source and behavior review-required. The switch needs an unknown/default branch and focused generated-client evidence.

**Decisive evidence:** consumer declaration test

The important nuance is: That is only the first column. Source review regenerates representative Python and TypeScript consumers. Python receives a new presence-aware accessor. A TypeScript operator client configured to preserve defaults and oneof metadata continues to compile. An exhaustive object-shape assertion in a handwritten client fails because it incorrectly treated the response as closed. The provider can call the change additive, but the consumer bug still needs repair.

## 6. Why should changing unary `GetRun` to server-streaming create a new method?

Streaming shape is part of the RPC method contract and generated signature. Changing it in place breaks stubs, lifecycle, retry, and backpressure behavior.

**Decisive evidence:** generated method signature diff

Under concurrency or failure, the distinction becomes: Adding a method is generally safe for existing clients but may be operationally unsafe if it bypasses authorization, quotas, or ownership. Removing or renaming a service or method changes the fully qualified RPC path and is breaking. Changing unary to streaming, client-streaming to bidirectional, or response streaming shape is a new method, not an in-place edit.

## 7. What must be reserved when a published field is removed?

Reserve both the numeric tag and the source name. The number protects binary history; the name protects source and JSON clarity.

**Decisive evidence:** reservation lint

The design remains honest only if: Never renumber enum values. Reserve removed values when the language and policy allow, and retain a zero unspecified value. Adding a value is usually binary-safe; it is not automatically source- or behavior-safe. Consumers must have an unknown-value path, and stored numeric values must remain interpretable.

## 8. Compare a golden binary fixture with a descriptor set.

A golden fixture proves concrete bytes and meaning for selected cases. A descriptor set inventories the declared schema and methods. Neither replaces the other.

**Decisive evidence:** descriptor/golden inventory

The consumer-facing consequence is: Descriptor sets provide machine-readable contract inventory independent of generated source languages. They support method catalogues, reflection comparisons, compatibility tools, and dynamic diagnostics. Course 7 includes a checked-in descriptor projection because protoc is not guaranteed in the dependency-light environment; the full proof regenerates it with pinned tools and compares the result.

## 9. Why can a string-to-bytes change be wire-readable but still breaking?

Both are length-delimited, but UTF-8 validation, generated types, JSON representation, and semantic interpretation change.

**Decisive evidence:** cross-language parse and JSON report

The operational consequence is: Changing string to bytes keeps the length-delimited wire type, but generated APIs, UTF-8 validation, JSON encoding, and semantic meaning change. Message and bytes fields also share a wire type but cannot be substituted safely. Fixed-width numeric changes can preserve bytes while changing signedness or floating interpretation.

## 10. What does Buf breaking analysis prove, and what does it not prove?

It proves configured structural and repository-relative compatibility rules. It does not prove runtime behavior, authorization, status policy, deadlines, or consumer assumptions.

**Decisive evidence:** Buf/local capability matrix

The strongest engineering interpretation is: Buf lint and breaking-change checks provide mature structural rules and repository-relative compatibility policies. They are valuable independent evidence, but they do not prove application behavior, status mapping, deadline safety, authorization, or generated runtime support. The course's local checker intentionally covers a narrower deterministic subset and reports its scope.

## 11. Why is creating a v2 package not a substitute for migration planning?

A major package still requires coexistence, client migration, data interpretation, observability, and retirement. It only makes incompatibility explicit.

**Decisive evidence:** v1/v2 migration plan

The defect-oriented view is: Package names are part of method identity. Moving a message or service to another package changes generated symbols and RPC paths even when fields are copied. Prefer a new versioned package such as bijux.analysis.v2 for an intentionally incompatible surface. Keep old and new services available through a migration window.

## 12. Define a release gate for an additive optional response field.

Require a new tag, explicit presence semantics, old-client parse proof, generated source builds, ProtoJSON review, no changed old bytes where promised, and behavioral tests showing old consumers remain correct.

**Decisive evidence:** accepted additive candidate report

Across the Python and TypeScript tracks, the invariant is: A candidate RPC 1.1 release adds optional string diagnostic summary = 10 to AnalysisRun. The wire review sees a fresh tag with the same message package and no changed old fields. Old binary readers can ignore tag 10. New readers can parse old bytes with the field absent. The change is wire-compatible.
