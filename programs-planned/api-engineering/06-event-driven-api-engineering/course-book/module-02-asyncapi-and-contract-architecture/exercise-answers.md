# Reference Answers — Module 02: Worked answers — Module 02 — AsyncAPI, CloudEvents, and Contract Architecture

Read after attempting all twelve AsyncAPI, CloudEvents, and Contract Architecture exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Correct an operation direction

The analytics application receives `AnalysisRunCompleted`, so its operation action is `receive`. AsyncAPI describes what the named application does. The fact that the broker sends bytes to the socket does not make the consumer a sender. A separate producer application document would use `send` for the same channel.

## 2. Separate three identities

Use a logical channel such as `analysisRunLifecycle`, a physical subject such as `analysis.events.run.completed.v1`, and semantic type `org.bijux.analysis.run.completed.v1`. The subject may change with broker topology, the logical channel may be reorganized in documentation, and the event type changes only for a semantic major version. They should not be one mutable string.

## 3. Design a message fragment

The fragment needs a stable message name/title, content type, correlation and profile metadata, a reference to the failed-run payload schema, and at least one complete example. The entry document references it from allowed channel messages and operations. The catalogue adds owner, source, partition, classification, retention, and replay policy. No one file carries all governance.

## 4. Validate in layers

The envelope profile fails because `tenantid` is required for authorization and routing policy. A valid `data` object only proves event-specific shape. Dispatch must occur only after both envelope and payload validation; otherwise a cross-tenant or unowned message can reach a type-correct handler.

## 5. Choose a schema URI

Use a stable absolute versioned URI as the public `dataschema`. Map that identity to a repository-controlled file during offline proof. A relative filename changes meaning with base location, while a mutable raw URL makes builds depend on external content and branch state.

## 6. Close a public payload

`additionalProperties: false` is appropriate when the message has a deliberate finite public shape and unknown fields would signal producer drift. If controlled extensibility is required, define an `extensions` object with namespacing, value constraints, and a compatibility policy. Leaving the entire payload open makes accidental private fields valid.

## 7. Audit an example

The path leaks implementation topology and may expose tenant storage layout. The bearer token is a live-secret disclosure and can enter generated docs and source history. Both may violate the payload schema and data-classification policy. Replace them with stable artifact identifiers and synthetic non-secret examples, then run secret scanning and example validation.

## 8. Model a command and an event

`StartAnalysis` is sent by a requester and received by one logical control-plane handler; it may be rejected and has task-oriented retention. `AnalysisRunStarted` is sent by the authoritative owner after commit and may be received by many consumers; consumers cannot make the historical fact false. Its retention follows replay and audit needs.

## 9. Define local proof scope

A defensible claim is: “The course validator parsed the AsyncAPI 3.1 source with duplicate-key detection, resolved all local message and schema references offline, checked the course envelope profile, and validated packaged examples. It did not independently implement every AsyncAPI normative rule or execute NATS protocol bindings.”

## 10. Plan a multi-document layout

Keep API identity, servers, channels, operations, and component indexes in the entry document. Put each public message in one fragment, each payload in one JSON Schema, and realistic complete instances in examples. Put owner, retention, classification, replay policy, and partition rationale in the catalogue. This balances reviewability and reference depth.

## 11. Protect operation identity

Generated clients, documentation links, policy rules, metrics, and governance inventories can key on operation ID. Renaming it breaks those consumers even if wire traffic remains valid. Treat the ID as a public stable identifier and deprecate or migrate it deliberately.

## 12. Review a binding

The subject/address and protocol-level binding fields belong in the contract when consumers need them. A particular queue-group instance count, redelivery threshold, or deployment replica count belongs in operational configuration unless it is part of the public service guarantee. Do not encode mutable deployment policy as universal interface semantics.
