# Worked answers — Protobuf Modeling, Presence, and Semantic Types

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Why should `CreateRunRequest` not mirror the analysis_runs table?

A persistence row contains internal ownership, retry, and bookkeeping fields, while the request describes one application decision. Direct mirroring enables mass assignment and couples the public contract to storage.

**Decisive evidence:** request-to-command mapping review

## 2. Model `result_summary` so that absent and present-empty remain distinguishable.

Declare `optional string result_summary`. Enforce state-dependent invariants separately: completion may carry a present empty value; nonterminal states must leave it absent.

**Decisive evidence:** presence vector and state invariant test

## 3. Why must the zero value of `RunState` be unspecified?

`RUN_STATE_UNSPECIFIED = 0` makes omission detectable. If queued were zero, malformed or old messages would silently request a real state.

**Decisive evidence:** omitted-enum vector

## 4. A consumer uses an exhaustive switch on an enum. How should an enum addition be classified?

Review-required. It is wire-additive, but exhaustive source consumers may fail or fall into unsafe default behavior. Consumer evidence decides promotion.

**Decisive evidence:** consumer compatibility matrix

## 5. Differentiate a resource name, request identifier, trace identifier, and lease generation.

A resource name identifies durable state; a request identifier deduplicates intent; a trace identifier follows one execution; a lease generation fences one attempt. They have different creators and lifetimes.

**Decisive evidence:** identity ownership table

## 6. Why is a JavaScript `number` unsafe for every Protobuf `int64`?

IEEE-754 numbers exactly represent integers only through 2^53−1. Protobuf 64-bit fields exceed that range, so numeric coercion can merge distinct values.

**Decisive evidence:** int64 boundary vector

## 7. Choose a representation for `revision` in the TypeScript application boundary and justify it.

Use a decimal string at the transport/JSON boundary and `bigint` internally where arithmetic is required. Validate the full signed or unsigned range before conversion.

**Decisive evidence:** cross-language round-trip

## 8. When is `oneof` appropriate for `UploadDatasetRequest`?

The upload stream carries mutually exclusive frame roles: one metadata frame or one bytes chunk. `oneof` makes invalid simultaneous alternatives unrepresentable in generated APIs.

**Decisive evidence:** oneof frame validation

## 9. What failure can occur when an existing field is moved into a `oneof`?

Presence and clearing semantics change. Old unknown data can be discarded when another member is set, and source APIs change even if tags remain wire-readable.

**Decisive evidence:** wire/source compatibility report

## 10. Design validation rules for an arbitrary metadata map.

Allow only governed keys, normalize names, bound key/value length and entry count, reject sensitive keys, and define duplicate behavior before serialization.

**Decisive evidence:** metadata abuse test

## 11. Choose between `Timestamp`, `Duration`, and a named integer field for three time concepts.

Use `Timestamp` for a wall-clock creation instant, `Duration` for a retry interval, and `lease_expires_unix_ms` only where the protocol explicitly requires Unix milliseconds.

**Decisive evidence:** semantic-type review

## 12. What does the Editions 2024 frontier prove if the local generator cannot compile it?

It proves a reviewed standards-frontier design and documents intended feature settings. It does not prove parser, generator, or runtime support; the capability matrix must say not executed.

**Decisive evidence:** tool capability matrix
