# Module 03 — Wire Format, Unknown Fields, and Compatibility Discipline

> **Program stage:** Course 7 of 10 — Engineer typed internal invocation and streaming.

> **Central question:** How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?

## Where this module fits

Module 02 produced **Complete the Analysis RPC 1.0 message model, publish cross-language presence and integer vectors, and document every field whose absence changes behavior**. This module extends that result by asking: **How can an RPC contract evolve without corrupting old data, breaking generated clients, or creating behavior that is wire-readable but operationally unsafe?**

The new capstone increment is **Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes**. It becomes the prerequisite for **Unary RPCs, Metadata, Status, and Rich Errors**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Explain how field numbers and wire types determine binary compatibility.
- Reserve removed field numbers and names and reject reuse.
- Classify changes across wire, source, JSON, and behavioral dimensions.
- Reason about unknown-field preservation and loss in proxies, stores, and language runtimes.
- Evaluate enum, oneof, map, service, method, and streaming-shape changes.
- Combine local semantic checks, golden bytes, generated-client builds, and Buf compatibility evidence.

## Capstone increment

Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes.

## Field numbers are the durable wire identity

Protobuf does not put field names on the binary wire. It encodes field numbers and wire types. Once a field is published, its number is the durable identity. Renaming a field can leave binary compatibility intact while breaking source and ProtoJSON consumers. Reusing a removed number for a new meaning can make retained bytes parse as the wrong value—one of the most dangerous changes in a schema-driven system.

When removing a field, reserve both its number and source name. The number protects binary history; the name protects future source authors from accidentally recreating an ambiguous JSON or generated API surface. The course compatibility checker rejects duplicate and reused tags, but a linter cannot infer semantic equivalence. Reviewers must compare the old and new meaning, not only the syntax.

Choose tags deliberately. Frequently used fields may benefit from lower numbers because tags 1–15 encode compactly, but do not churn tags for marginal size savings. Leave gaps only with a documented allocation policy. Stability is more valuable than a perfectly packed source file.

## Wire types make some source changes deceptive

A field key combines the number with a wire type. Varints, fixed-width values, length-delimited data, and groups have different encodings. Some source-type changes share a wire type and appear binary-readable but reinterpret values. `int32`, `uint32`, `bool`, and enums all use varints, yet changing among them can alter negative values, validation, and meaning. `int32` to `sint32` is especially unsafe because zig-zag encoding changes the bytes' interpretation even though both are integer concepts.

Changing `string` to `bytes` keeps the length-delimited wire type, but generated APIs, UTF-8 validation, JSON encoding, and semantic meaning change. Message and bytes fields also share a wire type but cannot be substituted safely. Fixed-width numeric changes can preserve bytes while changing signedness or floating interpretation.

Compatibility review therefore begins with wire evidence but never ends there. The release report records old type, new type, wire type, allowed value domain, and downstream behavior. A change that merely parses is not automatically safe.

## Unknown fields are a compatibility resource

An older consumer may receive a newer field it does not know. A well-behaved binary runtime can preserve that field when parsing and reserializing the message, allowing an old intermediary to forward new data without destroying it. But preservation is not universal across transformations. Converting to a domain object, rebuilding a message, passing through JSON, or using certain dynamic libraries may drop unknown fields.

Decide whether the application requires transparent forwarding. A control service that reads a request and constructs a new command does not promise to preserve arbitrary unknown request fields. A generic envelope store or replay archive may need exact original bytes. The contract and evidence class must distinguish semantic processing from byte-preserving forwarding.

Test the supported path. Inject an unknown tag into a golden message, parse it in Python and TypeScript, perform the intended operation, and compare output bytes. Do not make a platform-wide claim based on a single runtime's default behavior.

## Four compatibility dimensions

**Wire compatibility** asks whether old and new binaries can parse each other's bytes without misinterpretation. **Source compatibility** asks whether existing generated code still compiles and behaves under regeneration. **ProtoJSON compatibility** asks whether names, numeric representations, enum text, and JSON field mappings remain usable. **Behavioral compatibility** asks whether the operation still means what consumers rely on.

Renaming `dataset_name` while retaining tag 3 may be binary compatible, source breaking after regeneration, JSON breaking for clients that send the old key, and behaviorally neutral. Adding an enum value is wire additive but can break exhaustive source code and business assumptions. Increasing a maximum page or chunk size may be schema-neutral yet behaviorally affect memory and scheduling. Changing default deadline policy may not touch the `.proto` file at all but still be a breaking service-profile change.

Every release candidate gets a four-column classification. “Compatible” without a dimension is an incomplete statement.

## Enums and oneof evolution

Never renumber enum values. Reserve removed values when the language and policy allow, and retain a zero unspecified value. Adding a value is usually binary-safe; it is not automatically source- or behavior-safe. Consumers must have an unknown-value path, and stored numeric values must remain interpretable.

Adding a new `oneof` alternative is often wire-additive. Removing one is breaking. Moving an existing field into a new or existing `oneof` changes presence and mutual-exclusion behavior. Adding multiple previously independent fields to one `oneof` can cause old fields to clear when parsed together. Splitting or merging alternatives can also confuse old intermediaries that preserve unknown bytes.

Golden fixtures should include known and unknown enum values and each union alternative. Compatibility tests inspect semantic outcomes, not only parser success.

## Service and method evolution

Adding a method is generally safe for existing clients but may be operationally unsafe if it bypasses authorization, quotas, or ownership. Removing or renaming a service or method changes the fully qualified RPC path and is breaking. Changing unary to streaming, client-streaming to bidirectional, or response streaming shape is a new method, not an in-place edit.

Package names are part of method identity. Moving a message or service to another package changes generated symbols and RPC paths even when fields are copied. Prefer a new versioned package such as `bijux.analysis.v2` for an intentionally incompatible surface. Keep old and new services available through a migration window.

Do not create `v2` merely to avoid compatibility reasoning. A major version duplicates support burden and requires client migration evidence. The release gate demands a reason and retirement plan.

## Golden bytes and descriptors

Golden binary fixtures make wire assumptions reviewable. For each important message, store canonical bytes, a human-readable semantic projection, the source schema digest, and the runtime versions used. A golden file is not a snapshot to update casually. A change must explain whether the bytes should remain identical, remain parseable with equivalent meaning, or intentionally change under a new version.

Descriptor sets provide machine-readable contract inventory independent of generated source languages. They support method catalogues, reflection comparisons, compatibility tools, and dynamic diagnostics. Course 7 includes a checked-in descriptor projection because `protoc` is not guaranteed in the dependency-light environment; the full proof regenerates it with pinned tools and compares the result.

Golden bytes and descriptors complement each other: one proves concrete wire cases, the other proves the declared schema graph.

## Buf and local proof have different jobs

Buf lint and breaking-change checks provide mature structural rules and repository-relative compatibility policies. They are valuable independent evidence, but they do not prove application behavior, status mapping, deadline safety, authorization, or generated runtime support. The course's local checker intentionally covers a narrower deterministic subset and reports its scope.

The release ladder runs: parse and local schema invariants; golden-wire cases; Python and TypeScript generated or semantic builds; descriptor inventory; Buf lint and breaking checks when available; and behavioral conformance. A missing external tool is recorded as not executed, never transformed into a pass.

Planted candidates demonstrate proof sensitivity. The checker must reject tag reuse, enum renumbering, field removal without reservation, and unary-to-streaming mutation. If a proof cannot detect its assigned defect, the proof is not trusted.

## Compatibility is a consumer obligation too

Providers own safe evolution, but consumers must also handle additive change. Clients should ignore fields they do not need, preserve unknown enum numbers where the runtime permits, avoid exhaustive assumptions without a fallback, and use generated APIs according to supported presence semantics. A consumer that treats every response as a closed JSON object may break on an additive field even when the Protobuf contract is compatible.

The course includes consumer declarations: language, generator, version, used methods, enum policy, ProtoJSON use, unknown-field requirement, and upgrade cadence. Release review identifies which consumers require regeneration or focused tests. This turns “probably compatible” into a finite evidence problem.

Course 10 will use the same declarations during a strangler migration. Compatibility is not a one-time schema property; it is a managed relationship among producers, consumers, retained bytes, and operational policy.

## Worked release review: adding diagnostic summary

A candidate RPC 1.1 release adds `optional string diagnostic_summary = 10` to `AnalysisRun`. The wire review sees a fresh tag with the same message package and no changed old fields. Old binary readers can ignore tag 10. New readers can parse old bytes with the field absent. The change is wire-compatible.

That is only the first column. Source review regenerates representative Python and TypeScript consumers. Python receives a new presence-aware accessor. A TypeScript operator client configured to preserve defaults and oneof metadata continues to compile. An exhaustive object-shape assertion in a handwritten client fails because it incorrectly treated the response as closed. The provider can call the change additive, but the consumer bug still needs repair.

ProtoJSON review checks the emitted key and absence behavior. A client that hashes raw JSON responses would see a different representation and was relying on an unsupported property. A client that ignores unknown members remains correct. Behavioral review asks whether diagnostic text is safe, bounded, authorized, and stable enough for consumers. If it is merely operator-oriented information, it may not belong in the normal response at all. Compatibility cannot answer product design.

Now compare three rejected candidates. Reusing tag 7 after removing `result_summary` can make retained bytes parse as a new diagnostic code. Renumbering `RUN_STATE_COMPLETED` changes the meaning of stored numeric values. Renaming `dataset_name` while keeping tag 3 preserves binary parsing but breaks generated accessors and ProtoJSON keys. Each failure occupies a different compatibility dimension.

Unknown-field evidence is also path-specific. An old Python message may parse and reserialize tag 10 intact. If the application maps the message into a domain object and constructs a new response, the unknown field is intentionally lost. That is acceptable for a semantic endpoint but not for a transparent relay or byte-preserving archive. The release claim names the path rather than claiming universal preservation.

The final release report joins schema analysis with consumer declarations and golden bytes. It states: wire compatible; source compatible for declared generated consumers; ProtoJSON additive with one repaired strict consumer; behavior review approved under a bounded operator-visible policy. It also records Buf as not executed when unavailable. This is what an honest compatibility decision looks like: several precise claims, no magical green “compatible” badge.

## Implementation reading

Read `capstone/contracts/compatibility-policy.yaml`, the golden fixtures under `capstone/shared/golden/`, and the descriptor projection. Compare `scripts/compatibility_check.py` with optional Buf routes. The local checker declares its limits; generated-client and behavioral proofs carry the remaining claims.

## Failure checklist

- Has any published field number or enum number been reused?
- Does a source-compatible change reinterpret the same wire bytes?
- Will ProtoJSON clients survive field or enum-name changes?
- Does an old intermediary need to preserve unknown bytes?
- Has a unary or streaming method shape changed in place?
- Which concrete consumers and retained fixtures were tested?

## Transition

After preserving the checkpoint evidence, continue to **Unary RPCs, Metadata, Status, and Rich Errors**. Do not progress while the non-compensable gate remains unresolved.

## Module synthesis

You are ready to leave this module when you can **explain how field numbers and wire types determine binary compatibility, reserve removed field numbers and names and reject reuse, and classify changes across wire, source, JSON, and behavioral dimensions** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Renumber an enum value and observe golden semantic failure** and requiring the following oracle: **The additive candidate is accepted only with consumer evidence. Tag reuse, enum renumbering, and method-shape mutation are rejected. Reports identify compatibility dimension and affected consumers rather than returning one undifferentiated boolean.**

The cumulative platform now includes **Publish Analysis RPC compatibility policy 1.0, golden wire fixtures, and a release report that accepts one additive candidate while rejecting unsafe tag, enum, and method-shape changes**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Unary RPCs, Metadata, Status, and Rich Errors](../module-04-unary-rpcs-metadata-status-and-rich-errors/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
