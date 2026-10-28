# Reference Answers — Module 01: Worked answers — Module 01 — Event Thinking, Ownership, and Message Taxonomy

Read after attempting all twelve Event Thinking, Ownership, and Message Taxonomy exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Classify the run-submission flow

The HTTP submission is a synchronous command at the public boundary because it can be rejected and must return an authoritative acceptance result. The durable job request is an internal command for one worker handler. `AnalysisRunRequested` or `Queued` is an integration event because the owner has committed the fact and multiple consumers may observe it. Lease acquisition is an internal domain/coordination event unless an independent contract requires it; publishing it publicly would expose worker mechanics. Completion notification is a notification driven by the `AnalysisRunCompleted` fact. The decisive evidence is who may reject each message and which durable row proves the state.

## 2. Reject an unnecessary event

`ProjectViewed` should not enter the public event API merely because it can be emitted. It creates retention, privacy, compatibility, and ownership obligations without a consumer outcome. Keep local access telemetry under the reliability/analytics profile. Reconsider only when a named independent consumer, lawful purpose, retention rule, and stable semantic definition exist. Endpoint logs are not automatically business events.

## 3. Repair an imperative event

`generate.artifact` is imperative and therefore command-shaped. If one artifact component is instructed to produce output, use `GenerateArtifact` on a command channel. After durable publication succeeds, the artifact owner emits `org.bijux.analysis.artifact.published.v1`. The command can be rejected or retried; the event records the accepted fact.

## 4. Find the authoritative source

The control plane should own `AnalysisRunCompleted` because it owns the run state and can atomically persist completion, artifact references, and the outbox row. The worker reports a result through an internal command/result boundary. If the worker publishes completion independently, a crash between publication and control-plane commit can create a fact that the source of truth does not support.

## 5. Separate five identities

Use a fresh UUID for the event occurrence; `analysis-runs/run-123` as subject; the user journey UUID as correlation ID; the accepted completion-result command or preceding event ID as causation ID; and `run-123` as partition key. Event ID supports deduplication, subject names the entity, correlation links the journey, causation builds the direct graph, and partition key constrains order. Reusing one value would erase at least one distinction.

## 6. Choose event granularity

Separate facts give consumers precise subscriptions, simpler schemas, clearer authorization, and additive evolution. They also increase catalogue and operation count. A broad union reduces type count but makes every consumer depend on a volatile discriminated schema and can blur retention and ownership. For the small, stable run state machine, separate lifecycle facts are the stronger contract.

## 7. Protect the private model

Publish stable failure classification, run ID, safe reason code, terminal time, and perhaps attempt count if it is a supported consumer fact. Do not publish lease tokens, raw owner records, stack traces, or internal exception text. Retry counters belong only if the event contract defines their meaning independent of the current worker implementation. The schema and security classification—not convenience—decide.

## 8. Keep a synchronous boundary

Tenant ownership is an immediate authorization precondition. Accepting the command and waiting for an event consumer to deny it would create a time window in which unauthorized work may begin. Perform the check in the request transaction. An audit event can record the decision after it is made, but cannot become the decision point.

## 9. Distinguish domain and integration events

An internal event might carry an `ArtifactRecord`, storage transaction ID, temporary path, checksum object, and publication phase. The integration event contains artifact ID, run ID, media type, size, checksum string, publication time, tenant, and stable schema reference. Temporary paths, storage internals, and object types are removed because consumers do not own those concepts.

## 10. Evaluate temporal decoupling

Billing can subscribe to `AnalysisRunCompleted` and react later because billing delay does not alter the fact of completion. Artifact metadata must remain in the same authoritative transaction or completion protocol because a completion event that references missing artifacts would be false. The separation is based on invariant ownership, not on which code is slower.

## 11. Identify a notification

The durable fact is `AnalysisRunCompleted`. A notification consumer may translate that event into a one-recipient `SendCompletionEmail` command or directly call an email adapter under its own retry policy. The email itself is not the authoritative completion event. Calling every outbound request an event hides that it has one intended handler and may fail.

## 12. Write the publication test

Ask: What durable fact became true? Who owns and can prove it? Which independent consumer needs delayed access? Which duplicate, ordering, and replay failures must be tolerated? Can the meaning remain stable for the retention period? If no owner can identify a committed scan result, reject `DatasetScanned`; do not publish an observation that no source of truth can defend.
