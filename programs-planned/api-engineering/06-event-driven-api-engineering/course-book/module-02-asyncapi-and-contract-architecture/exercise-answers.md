# Worked Answers — Module 02: AsyncAPI, CloudEvents, and Contract Architecture

Use these solutions to audit your reasoning for **AsyncAPI, CloudEvents, and Contract Architecture**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Correct an operation direction

The analytics application receives `AnalysisRunCompleted`, so its operation action is `receive`. AsyncAPI describes what the named application does. The fact that the broker sends bytes to the socket does not make the consumer a sender. A separate producer application document would use `send` for the same channel.

The chapter’s decisive distinction is this: A consumer application document says it “sends” AnalysisRunCompleted because the broker sends the record to the process. AsyncAPI operations are from the application perspective: the consumer receives the event. Reverse the operation action and keep broker delivery mechanics in the binding or runtime documentation.

## 2. Separate three identities

Use a logical channel such as `analysisRunLifecycle`, a physical subject such as `analysis.events.run.completed.v1`, and semantic type `org.bijux.analysis.run.completed.v1`. The subject may change with broker topology, the logical channel may be reorganized in documentation, and the event type changes only for a semantic major version. They should not be one mutable string.

In the cumulative capstone, the rule becomes concrete: The event type was set to analysis.events.completed, exactly matching the subject. A later subject hierarchy change would therefore alter semantic identity. Keep the stable reverse-DNS event type in the envelope and document the physical subject separately in the channel address.

## 3. Design a message fragment

The fragment needs a stable message name/title, content type, correlation and profile metadata, a reference to the failed-run payload schema, and at least one complete example. The entry document references it from allowed channel messages and operations. The catalogue adds owner, source, partition, classification, retention, and replay policy. No one file carries all governance.

A useful way to reason about the boundary is: One monolithic AsyncAPI file becomes difficult to review, while hundreds of tiny fragments create a reference maze. The capstone keeps the entry document, one message fragment per public type, and one payload schema per type. Shared envelope rules live in the course profile rather than being copied into every payload schema.

## 4. Validate in layers

The envelope profile fails because `tenantid` is required for authorization and routing policy. A valid `data` object only proves event-specific shape. Dispatch must occur only after both envelope and payload validation; otherwise a cross-tenant or unowned message can reach a type-correct handler.

The implementation consequence is: The envelope proves that the message has valid identity, source, type, time, schema reference, tenant, correlation, causation, partition, and content metadata. The payload schema proves that the event-specific data object has required fields, types, ranges, and additional-property policy.

## 5. Choose a schema URI

Use a stable absolute versioned URI as the public `dataschema`. Map that identity to a repository-controlled file during offline proof. A relative filename changes meaning with base location, while a mutable raw URL makes builds depend on external content and branch state.

The important nuance is: A JSON Schema $id is an identifier and reference base, not merely a filename. dataschema identifies the payload schema that the producer claims to use. Relative filesystem references are acceptable inside the source tree, but emitted event metadata should use stable absolute schema URIs.

## 6. Close a public payload

`additionalProperties: false` is appropriate when the message has a deliberate finite public shape and unknown fields would signal producer drift. If controlled extensibility is required, define an `extensions` object with namespacing, value constraints, and a compatibility policy. Leaving the entire payload open makes accidental private fields valid.

Under concurrency or failure, the distinction becomes: additionalProperties was omitted, so a producer included a worker lease token and exception stack. The payload remained structurally valid. Close public schemas deliberately and use an explicit extension object only where open content is an actual contract requirement.

## 7. Audit an example

The path leaks implementation topology and may expose tenant storage layout. The bearer token is a live-secret disclosure and can enter generated docs and source history. Both may violate the payload schema and data-classification policy. Replace them with stable artifact identifiers and synthetic non-secret examples, then run secret scanning and example validation.

The design remains honest only if: The completed example contains durationMs: "8421" as a string. The renderer displays it, but generated consumers infer an integer. Add example validation to the proof and fix the example; documentation visibility is not schema conformance.

## 8. Model a command and an event

`StartAnalysis` is sent by a requester and received by one logical control-plane handler; it may be rejected and has task-oriented retention. `AnalysisRunStarted` is sent by the authoritative owner after commit and may be received by many consumers; consumers cannot make the historical fact false. Its retention follows replay and audit needs.

The consumer-facing consequence is: The contract begins with the application’s perspective. The Analysis command publisher sends StartAnalysis to a command channel. The control plane receives it. The control plane then sends lifecycle events that consumers receive. An operation’s action is interpreted from the described application, so “send” and “receive” must not be copied mechanically from the remote peer’s viewpoint.

## 9. Define local proof scope

A defensible claim is: “The course validator parsed the AsyncAPI 3.1 source with duplicate-key detection, resolved all local message and schema references offline, checked the course envelope profile, and validated packaged examples. It did not independently implement every AsyncAPI normative rule or execute NATS protocol bindings.”

The operational consequence is: The dependency-light validator checks YAML structure, duplicate keys, AsyncAPI version, channel and operation references, message references, profile-required fields, schema resolution, examples, and a course-specific semantic policy. It does not claim to be a complete implementation of every AsyncAPI rule or every protocol binding.

## 10. Plan a multi-document layout

Keep API identity, servers, channels, operations, and component indexes in the entry document. Put each public message in one fragment, each payload in one JSON Schema, and realistic complete instances in examples. Put owner, retention, classification, replay policy, and partition rationale in the catalogue. This balances reviewability and reference depth.

The strongest engineering interpretation is: Each public message has at least one complete example containing both envelope metadata and data. Examples must validate against the same schemas as production messages. They also expose ambiguities that type definitions alone can hide: timestamp precision, subject format, URI spelling, null handling, partition keys, and safe error detail.

## 11. Protect operation identity

Generated clients, documentation links, policy rules, metrics, and governance inventories can key on operation ID. Renaming it breaks those consumers even if wire traffic remains valid. Treat the ID as a public stable identifier and deprecate or migrate it deliberately.

The defect-oriented view is: Validating only the payload allows a forged source or missing tenant. Validating only the envelope allows an AnalysisRunCompleted event with no run ID or a negative duration. The contract proof resolves the message reference, applies the common envelope profile, then validates data against the referenced JSON Schema.

## 12. Review a binding

The subject/address and protocol-level binding fields belong in the contract when consumers need them. A particular queue-group instance count, redelivery threshold, or deployment replica count belongs in operational configuration unless it is part of the public service guarantee. Do not encode mutable deployment policy as universal interface semantics.

Across the Python and TypeScript tracks, the invariant is: The physical NATS subject is an address. The logical channel is an API element. The event type is a semantic identifier. They may be related, but merging all three makes later transport migration and catalogue governance harder.
