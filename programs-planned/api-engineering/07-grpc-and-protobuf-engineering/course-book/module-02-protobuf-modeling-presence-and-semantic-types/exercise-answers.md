# Worked Answers — Module 02: Protobuf Modeling, Presence, and Semantic Types

Use these solutions to audit your reasoning for **Protobuf Modeling, Presence, and Semantic Types**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should `CreateRunRequest` not mirror the analysis_runs table?

A persistence row contains internal ownership, retry, and bookkeeping fields, while the request describes one application decision. Direct mirroring enables mass assignment and couples the public contract to storage.

**Decisive evidence:** request-to-command mapping review

The chapter’s decisive distinction is this: This separation prevents two recurring failures. Mass assignment occurs when a generated request is persisted directly and caller-controlled fields become trusted. Contract ossification occurs when internal storage changes require public field changes. Generated messages should be translated at the transport boundary into application commands and results. The mapping is visible, reviewed, and tested.

## 2. Model `result_summary` so that absent and present-empty remain distinguishable.

Declare `optional string result_summary`. Enforce state-dependent invariants separately: completion may carry a present empty value; nonterminal states must leave it absent.

**Decisive evidence:** presence vector and state invariant test

In the cumulative capstone, the rule becomes concrete: Use optional when the application must distinguish absence from a present scalar. In AnalysisRun, result summary is absent while work has not produced a result; an empty summary can still be a deliberate completed value. failure code is absent for non-failed runs. Presence is not a substitute for state invariants: a completed run must satisfy the rule that failure information is absent, and a failed run must not claim a successful result.

## 3. Why must the zero value of `RunState` be unspecified?

`RUN_STATE_UNSPECIFIED = 0` makes omission detectable. If queued were zero, malformed or old messages would silently request a real state.

**Decisive evidence:** omitted-enum vector

A useful way to reason about the boundary is: Every enum begins with a zero value. Make it an explicit UNSPECIFIED value and reject it where the operation requires a choice. A meaningful state such as QUEUED = 0 makes an omitted field silently become a real state. That masks old-client behavior, malformed messages, and mapping defects.

## 4. A consumer uses an exhaustive switch on an enum. How should an enum addition be classified?

Review-required. It is wire-additive, but exhaustive source consumers may fail or fall into unsafe default behavior. Consumer evidence decides promotion.

**Decisive evidence:** consumer compatibility matrix

The implementation consequence is: Enum values are wire numbers with source names. Never renumber a published value, and do not reuse a removed number. Adding a new value is usually wire-compatible but can break exhaustive consumers. Course 7 therefore classifies enum additions as review-required unless consumers prove unknown-value handling. Python may preserve an unknown integer differently from generated TypeScript libraries; shared vectors must test what each supported runtime actually does.

## 5. Differentiate a resource name, request identifier, trace identifier, and lease generation.

A resource name identifies durable state; a request identifier deduplicates intent; a trace identifier follows one execution; a lease generation fences one attempt. They have different creators and lifetimes.

**Decisive evidence:** identity ownership table

The important nuance is: A resource name identifies durable state, for example projects/p-1/runs/r-9. A request identifier deduplicates one command intent. A trace identifier correlates telemetry. A correlation identifier groups a business workflow. A causation identifier links one message to the action that produced it. A worker assignment identifier identifies one leased attempt. A lease generation fences stale workers. A database row identifier may remain entirely private.

## 6. Why is a JavaScript `number` unsafe for every Protobuf `int64`?

IEEE-754 numbers exactly represent integers only through 2^53−1. Protobuf 64-bit fields exceed that range, so numeric coercion can merge distinct values.

**Decisive evidence:** int64 boundary vector

Under concurrency or failure, the distinction becomes: The course uses 64-bit values for revisions, stream sequence numbers, byte offsets, and lease expiry instants where the range is justified. TypeScript boundary models represent them as decimal strings or bigint internally; JSON evidence uses canonical decimal strings. Conversion rejects fractions, signs where forbidden, leading ambiguity, and values outside the declared range. Never use Number(value) merely to make a test pass.

## 7. Choose a representation for `revision` in the TypeScript application boundary and justify it.

Use a decimal string at the transport/JSON boundary and `bigint` internally where arithmetic is required. Validate the full signed or unsigned range before conversion.

**Decisive evidence:** cross-language round-trip

The design remains honest only if: Now consider revision. The database uses a bigint and the RPC uses int64 revision = 9. Python can represent all valid values. JavaScript cannot safely use a number above 2^53−1. The TypeScript adapter therefore accepts a canonical decimal string from the loader or a Long-like representation, validates the signed 64-bit range, and converts to bigint for arithmetic. The course’s JSON evidence also uses a decimal string.

## 8. When is `oneof` appropriate for `UploadDatasetRequest`?

The upload stream carries mutually exclusive frame roles: one metadata frame or one bytes chunk. `oneof` makes invalid simultaneous alternatives unrepresentable in generated APIs.

**Decisive evidence:** oneof frame validation

The consumer-facing consequence is: Use oneof for mutually exclusive wire alternatives, such as the first upload frame carrying metadata and later frames carrying bytes. It gives generated APIs an explicit union and prevents simultaneous alternatives. Adding fields to a published oneof is generally compatible on the wire, but moving an existing field into or out of a oneof can change presence and clearing behavior.

## 9. What failure can occur when an existing field is moved into a `oneof`?

Presence and clearing semantics change. Old unknown data can be discarded when another member is set, and source APIs change even if tags remain wire-readable.

**Decisive evidence:** wire/source compatibility report

The operational consequence is: Each vector records the source representation, expected binary digest, expected semantic projection, and whether ProtoJSON round-trip is part of the claim. The proof rejects libraries or options that coerce 64-bit values. It also detects generated-code settings that discard unknown fields when a compatibility workflow requires preservation.

## 10. Design validation rules for an arbitrary metadata map.

Allow only governed keys, normalize names, bound key/value length and entry count, reject sensitive keys, and define duplicate behavior before serialization.

**Decisive evidence:** metadata abuse test

The strongest engineering interpretation is: The proto comments and RPC catalogue define identity scope, creator, uniqueness boundary, retention, and whether the value is safe to expose. Tests verify that idempotency keys cannot be substituted for resource names and that stale generations cannot authorize completion.

## 11. Choose between `Timestamp`, `Duration`, and a named integer field for three time concepts.

Use `Timestamp` for a wall-clock creation instant, `Duration` for a retry interval, and `lease_expires_unix_ms` only where the protocol explicitly requires Unix milliseconds.

**Decisive evidence:** semantic-type review

The defect-oriented view is: A number without a unit is an eventual defect. Name units in fields when no standard semantic type exists: heartbeat interval ms, lease expires unix ms, offset bytes. For wall-clock instants that need calendar interoperability, use google.protobuf.Timestamp when supported by the generation profile. For durations, use google.protobuf.Duration. For monotonic local elapsed time, do not serialize a process clock as a timestamp.

## 12. What does the Editions 2024 frontier prove if the local generator cannot compile it?

It proves a reviewed standards-frontier design and documents intended feature settings. It does not prove parser, generator, or runtime support; the capability matrix must say not executed.

**Decisive evidence:** tool capability matrix

Across the Python and TypeScript tracks, the invariant is: The course does not label the frontier executable unless the local toolchain proves it. The capability matrix records parser, generator, runtime, and linter support separately. A learner may use a newer protoc or Buf toolchain to compile the frontier, but the baseline remains the source used by dependency-light proofs.
