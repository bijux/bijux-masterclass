# Worked answers — Wire Format, Unknown Fields, and Compatibility Discipline

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Why is reusing a removed field number more dangerous than reusing a local variable name?

Retained bytes encode the number, not the old name. Reuse can make historical data parse as a new semantic value without any syntax error.

**Decisive evidence:** tag-reuse golden fixture

## 2. Classify renaming a field while keeping its tag across four compatibility dimensions.

Binary wire can remain compatible; regenerated source breaks at the accessor name; ProtoJSON keys change; behavior may remain neutral if meaning is identical. The release is not simply compatible.

**Decisive evidence:** four-axis compatibility report

## 3. Why is `int32` to `sint32` unsafe despite both representing integers?

`sint32` uses zig-zag encoding while `int32` uses ordinary varint interpretation. Existing bytes produce different values, especially for negatives.

**Decisive evidence:** wire-type vector

## 4. When may an old intermediary safely drop unknown fields?

Only when the component semantically consumes and reconstructs the message and the contract does not promise transparent forwarding or exact-byte retention. A relay/archive may not drop them.

**Decisive evidence:** unknown-field forwarding test

## 5. Classify adding a new enum value for a TypeScript consumer with an exhaustive switch.

Wire-additive but source and behavior review-required. The switch needs an unknown/default branch and focused generated-client evidence.

**Decisive evidence:** consumer declaration test

## 6. Why should changing unary `GetRun` to server-streaming create a new method?

Streaming shape is part of the RPC method contract and generated signature. Changing it in place breaks stubs, lifecycle, retry, and backpressure behavior.

**Decisive evidence:** generated method signature diff

## 7. What must be reserved when a published field is removed?

Reserve both the numeric tag and the source name. The number protects binary history; the name protects source and JSON clarity.

**Decisive evidence:** reservation lint

## 8. Compare a golden binary fixture with a descriptor set.

A golden fixture proves concrete bytes and meaning for selected cases. A descriptor set inventories the declared schema and methods. Neither replaces the other.

**Decisive evidence:** descriptor/golden inventory

## 9. Why can a string-to-bytes change be wire-readable but still breaking?

Both are length-delimited, but UTF-8 validation, generated types, JSON representation, and semantic interpretation change.

**Decisive evidence:** cross-language parse and JSON report

## 10. What does Buf breaking analysis prove, and what does it not prove?

It proves configured structural and repository-relative compatibility rules. It does not prove runtime behavior, authorization, status policy, deadlines, or consumer assumptions.

**Decisive evidence:** Buf/local capability matrix

## 11. Why is creating a v2 package not a substitute for migration planning?

A major package still requires coexistence, client migration, data interpretation, observability, and retirement. It only makes incompatibility explicit.

**Decisive evidence:** v1/v2 migration plan

## 12. Define a release gate for an additive optional response field.

Require a new tag, explicit presence semantics, old-client parse proof, generated source builds, ProtoJSON review, no changed old bytes where promised, and behavioral tests showing old consumers remain correct.

**Decisive evidence:** accepted additive candidate report
