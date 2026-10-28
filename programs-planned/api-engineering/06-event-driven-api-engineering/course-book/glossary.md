# Glossary — Event-Driven API Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

## Acknowledgement

A protocol action that settles one delivery attempt and advances consumer progress according to broker policy.
It is not proof that an external business effect occurred unless the consumer’s transaction and evidence say so.

## AsyncAPI

A machine-readable description format for asynchronous application interfaces, including channels, operations,
messages, schemas, servers, bindings, and security.

## At-least-once delivery

A delivery policy that keeps a record eligible until acknowledgement, protecting against loss at the cost of
possible duplicate delivery.

## Causation ID

Identity of the command or event that directly caused another event.

## Channel

A logical communication location in an asynchronous API. A physical broker address or subject implements a
channel but is not identical to event type.

## CloudEvent

An event represented using the CloudEvents common attribute model. Course-specific extension attributes remain
profile policy.

## Command

A request for one logical handler to attempt an action. It expresses intent and may be rejected.

## Consumer effect version

Versioned identity of one durable outcome produced by a consumer. It participates in inbox deduplication and
replay isolation.

## Consumer group

A broker-side logical subscription whose instances share partitions and progress. Different business effects
normally use different groups.

## Correlation ID

Identity that links messages and operations belonging to a wider user or business journey.

## Dead letter

Durable evidence that automated handling stopped after a declared terminal policy. It requires ownership,
classification, repair, retention, and replay controls.

## Domain event

An internal application fact used to model one domain boundary. It is not automatically a public integration
event.

## Event

An immutable statement that an authoritative fact became true.

## Event API

The versioned public set of commands/events, envelopes, schemas, channels, ownership, delivery expectations,
security, replay, and lifecycle policy.

## Event time

The business time when the fact occurred, distinct from ingestion or processing time.

## Inbox

Durable consumer identity used in the same transaction as a business effect to suppress repeated application of
one event to one effect version.

## Integration event

A deliberately designed event published for independently deployed consumers.

## Message

The transported unit containing envelope metadata and payload. A message can carry a command, event, or other
interaction category.

## Outbox

A durable producer table or store written atomically with authoritative state to record publication intent.

## Partition

An ordered shard of a channel or stream. Order is generally comparable only inside one partition.

## Partition key

Stable domain identity used to assign related records to the same partition.

## Processing time

Time when a consumer handles a record, which may differ substantially from event time.

## Projection

Derived state built from events, usually replayable under a versioned effect identity.

## Replay

Controlled reprocessing of retained events under an explicit scope, target, consumer/effect version, side-effect
policy, bound, and operational budget.

## Retention

Policy defining how long broker/archive records remain available. It constrains replay and privacy obligations.

## Schema compatibility

Whether new producers, current consumers, and retained records remain mutually intelligible under declared
structural and semantic policy.

## Subject

Domain resource identity the event concerns. It is not the same as a NATS subject/address.

## Transactional outbox

Pattern that commits domain state and immutable publication intent in one local transaction.

## Upcaster

Deterministic representation translation from an older event schema/version to a newer consumer input. It must
not invent unavailable historical truth.

## Watermark

A stream-processing estimate that events earlier than a threshold are unlikely under normal conditions. It is
not proof that none will arrive.

## Window

A time-bounded grouping used for stream aggregation, such as tumbling, sliding, or session windows.
